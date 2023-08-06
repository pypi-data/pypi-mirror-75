# PySpark Setup
import os
from enum import Enum

import pyspark
from cassandra.cluster import Cluster

from .base import AutomatedPreparation


class ScalingMethod(Enum):
    Standard = 0
    MaxAbs = 1
    MinMax = 2


class SparkAutomatedPreparation(AutomatedPreparation):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._setup_spark()
        self.numeric_types = ["int", "long", "float", "decimal.Decimal"]

    def _setup_spark(self):
        os.environ['PYSPARK_PYTHON'] = 'python3'
        conf = pyspark.conf.SparkConf()
        sc = pyspark.context.SparkContext.getOrCreate(conf=conf)
        spark = pyspark.SQLContext(sc)
        self.spark = spark

    def get_df(self, backend, *args):
        if backend == "Cassandra":
            ksp, table = args
            df = self.spark.read.format("org.apache.spark.sql.cassandra").options(keyspace=ksp, table=table).load()
        else:
            raise RuntimeError(f"Spark backend {backend} not yet implemented.")
        return df

    def _replace_missing_data(self, df):
        from pyspark.sql.functions import when, lit

        for column in df.columns:
            df = df.withColumn(column, when(df[column].isin(self.missing_values), lit(None)).otherwise(df[column]))

        return df

    def _is_numeric(self, data_type):
        return data_type in self.numeric_types

    def _interpolate_missing_data(self, df, types):
        from pyspark.sql.functions import when, lit, desc

        for column in df.columns:
            if self._is_numeric(types[column]):
                # replace with the mean
                to_replace = df.select(mean(df[column])).collect()[0][0]
            else:
                # replace with the mode
                to_replace = df.groupBy(column).count().orderBy(desc("count")).collect()[0][0]

            df = df.withColumn(column, when(df[column].isNull(), lit(to_replace)).otherwise(df[column]))
            df = df.withColumn(column, when(df[column] == lit(None), lit(to_replace)).otherwise(df[column]))
            df = df.fillna(to_replace, subset=[column])

        return df

    def _detect_remove_outliers(self, df, types):
        from pyspark.sql.functions import stddev_pop, mean

        for column in df.columns:
            if self._is_numeric(types[column]):
                mean = df.select(mean(df[column])).collect()[0][0]
                std = df.select(stddev_pop(df[column])).collect()[0][0]

                threshold_outlier = (3 * std) + mean

                df = df.filter(df[column] < threshold_outlier).collect()

        return df

    def _one_hot_encode(self, df, column):
        from pyspark.ml import Pipeline
        from pyspark.ml.feature import StringIndexer, OneHotEncoder

        indexer = StringIndexer(inputCol=column, outputCol=column + "_labeled")
        one_hot_encoder = OneHotEncoder(inputCols=[column + "_labeled"],
                                                 outputCols=[column + "_onehotencoded"])

        pipeline = Pipeline().setStages([indexer, one_hot_encoder])
        pipeline_model = pipeline.fit(df)
        df = pipeline_model.transform(df)

        df = df.drop(column, column + "_labeled")

        return df

    def _label_encode(self, df, column):
        from pyspark.ml import Pipeline
        from pyspark.ml.feature import StringIndexer

        indexer = StringIndexer(inputCol=column, outputCol=column + "_labeled")

        pipeline = Pipeline().setStages([indexer])
        pipeline_model = pipeline.fit(df)
        df = pipeline_model.transform(df)

        df = df.drop(column)

        return df

    def _encode_categorical(self, df, types):
        if self.target_variable is None:
            to_exclude = []
        else:
            to_exclude = [self.target_variable]

        for column in set(df.columns).difference(to_exclude):
            if not self._is_numeric(types[column]):
                distinct_values = df.select(column).distinct().collect()

                if len(distinct_values) <= self.threshold_cardinality:
                    # one-hot encode low-cardinality categorical variables
                    df = self._one_hot_encode(df, column)
                else:
                    # label encode high-cardinality categorical variables
                    df = self._label_encode(df, column)

        return df

    def _assemble_df(self, df):
        from pyspark.ml.feature import VectorAssembler

        if self.target_variable is None:
            to_exclude = []
        else:
            to_exclude = [self.target_variable]

        vectorAssembler = VectorAssembler(inputCols=list(set(df.columns).difference(to_exclude)),
                                          outputCol="features")
        assembled_df = vectorAssembler.transform(df)

        to_return = ["features"]
        if self.target_variable is not None:
            to_return.append(self.target_variable)

        df = assembled_df.select(to_return)

        return df

    @staticmethod
    def get_scaling_options():
        return [scaling.name for scaling in ScalingMethod]

    def _scale_df(self, df):
        from pyspark.ml.feature import StandardScaler, MaxAbsScaler, MinMaxScaler

        scaler = None

        inputCol = "features"
        outputCol = "scaled_features"

        if self.scaling_method == ScalingMethod.Standard.value:
            scaler = StandardScaler(withMean=True, withStd=True, inputCol=inputCol, outputCol=outputCol)
        elif self.scaling_method == ScalingMethod.MaxAbs.value:
            scaler = MaxAbsScaler(inputCol=inputCol, outputCol=outputCol)
        elif self.scaling_method == ScalingMethod.MinMax.value:
            scaler = MinMaxScaler(min=0.0, max=1.0, inputCol=inputCol, outputCol=outputCol)

        if scaler is None:
            with open("scaling_log.txt", "a") as f:
                f.write(
                    f"{str(self.scaling_method)} {str(type(self.scaling_method))} != {str(ScalingMethod.Standard.value)} {str(type(ScalingMethod.Standard.value))}")
            raise RuntimeError("Scaler method not selected. This should not happen.")

        scaler_model = scaler.fit(df)
        df = scaler_model.transform(df)

        df = df.drop("features")
        df = df.withColumnRenamed("scaled_features", "features")

        return df

    def _perform_pca(self, df):
        from pyspark.ml.feature import PCA

        n_samples = df.count()
        n_features = len(df.select("features").collect()[0][0])
        n_components = min(n_samples, n_features)

        inputCol = "features"
        outputCol = "pca_features"

        pca = PCA(k=n_components, inputCol=inputCol, outputCol=outputCol)
        pca_model = pca.fit(df)

        accum_variance = 0

        for i, var in enumerate(pca_model.explainedVariance):
            accum_variance += var
            if accum_variance >= 0.95:
                components = i + 1
                break
        else:
            components = n_components

        if components != n_components:
            pca = PCA(k=components, inputCol=inputCol, outputCol=outputCol)
            pca_model = pca.fit(df)

        df = pca_model.transform(df)

        df = df.drop("features")
        df = df.withColumnRenamed("pca_features", "features")

        return df

    def automated_data_preparation(self, df, description, progress):
        types = {column: t for column, t in df.dtypes}

        try:
            # interpolate missing values
            if self.missing_values is not None:
                description.value = "Interpolating missing values..."
                df = self._replace_missing_data(df)
                df = self._interpolate_missing_data(df, types)
                progress.value += 1

            # detect and remove outliers
            if self.remove_outliers:
                description.value = "Removing outliers..."
                df = self._detect_remove_outliers(df, types)
                progress.value += 1

            # encode categorical variables
            if self.threshold_cardinality is not None:
                description.value = "Encoding categorical variables..."
                df = self._encode_categorical(df, types)
                progress.value += 1

            # needed for Spark
            description.value = "Assembling features"
            df = self._assemble_df(df)
            progress.value += 1

            # scale dataset
            if self.scaling_method is not None:
                description.value = "Scaling dataframe..."
                df = self._scale_df(df)
                progress.value += 1

            # perform PCA
            if self.do_PCA:
                description.value = "Performing PCA..."
                df = self._perform_pca(df)
                progress.value += 1

        except Exception as ex:
            with open("Automated_preparation_log.txt", "a") as f:
                f.write(str(ex))
            raise ex

        return df

    to_cql = {
        "bool": "boolean",
        "boolean": "boolean",
        "int": "int",
        "integer": "int",
        "float": "float",
        "double": "double",
        "object": "text",
        "string": "text"
    }

    def save_df(self, df, backend, args):
        if backend == "Cassandra":
            keyspace, table = args
            self._save_to_cassandra(df, keyspace, table)
        else:
            raise RuntimeError(f"Saving to {backend} not yet implemented.")

    def _save_to_cassandra(self, df, keyspace, table):
        cluster = Cluster([os.environ["CASSANDRA_SERVICE_SERVICE_HOST"]])
        # cluster = Cluster(["localhost"])
        session = cluster.connect()

        create_keyspace = f"CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH " \
                          "replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;"
        session.execute(create_keyspace)

        if self.target_variable is not None:
            to_select = ["features", self.target_variable]
        else:
            to_select = ["features"]

        n_features = len(df.select(to_select).collect()[0][0])

        create = f"CREATE TABLE {keyspace}.{table} " \
                 f"(id int PRIMARY KEY, column_{' double, column_'.join([str(i) for i in range(n_features)])} double"

        insert = f"INSERT INTO {keyspace}.{table} " \
                 f"(id, column_{', column_'.join([str(i) for i in range(n_features)])}"
        if self.target_variable is not None:
            insert += ", target"
        insert += f") VALUES (" + ", ".join(["?"] * (n_features + 1))  # + 1 for the id of the row

        if self.target_variable is not None:
            target_type = [t for name, t in df.dtypes if name == self.target_variable][0]
            cassandra_target_type = self.to_cql[target_type]
            create += f", target {cassandra_target_type}"
            insert += f", ?"

        create += ");"
        insert += ");"

        try:
            session.execute(create)
        except Exception as ex:
            with open("creating_table_log.txt", "a") as f:
                f.write(str(ex) + "\n" + create + "\n")
            raise ex

        try:
            insert_prepared = session.prepare(insert)
            for index, row in enumerate(df.select(to_select).collect()):
                data = [index] + [float(value) for value in row[0]]

                if self.target_variable is not None:
                    if cassandra_target_type == "boolean":
                        data += [bool(row[1])]
                    elif cassandra_target_type == "int":
                        data += [int(row[1])]
                    elif cassandra_target_type == "float" or cassandra_target_type == "double":
                        data += [float(row[1])]
                    elif cassandra_target_type == "text":
                        data += [str(row[1])]

                session.execute(insert_prepared, data)
        except Exception as ex:
            with open("inserting_data_log.txt", "a") as f:
                f.write(str(ex) + "\n" + insert + "\n")
                if "row" in locals():
                    f.write(str(row))
            raise ex
