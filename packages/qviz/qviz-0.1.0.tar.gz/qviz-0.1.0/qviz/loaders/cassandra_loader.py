import os

import pandas as pd
from cassandra.cluster import Cluster

from .base import Loader

to_cql = {
    "bool": "boolean",
    "int": "int",
    "int8": "int",
    "int32": "int",
    "int64": "bigint",
    "uint8": "int",
    "uint16": "int",
    "uint32": "int",
    "uint64": "bigint",
    "float": "float",
    "float16": "float",
    "float32": "float",
    "float64": "double",
    "object": "text"
}


class CassandraLoader(Loader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cluster = Cluster([os.environ.get("CASSANDRA_SERVICE_SERVICE_HOST", "127.0.0.1")])
        # self.cluster = Cluster(["localhost"])
        self.session = self.cluster.connect()

    def set_qbeast_index(self, cols=None):
        if cols is not None:
            create_index = f"CREATE CUSTOM INDEX IF NOT EXISTS {self.table + '_idx'} ON {self.keyspace}.{self.table} " \
                           f"({', '.join(cols)}) USING 'es.bsc.qbeast.index.QbeastIndex';"
            create_trigger = f"CREATE TRIGGER IF NOT EXISTS {self.table + 'trig'} ON {self.keyspace}.{self.table} " \
                             f"USING 'es.bsc.qbeast.index.QbeastTrigger';"

            self.session.execute(create_index)
            self.session.execute(create_trigger)

    def create_schema(self, keyspace, table):
        self.keyspace = keyspace
        self.table = table

        create_keyspace = f"CREATE KEYSPACE IF NOT EXISTS {self.keyspace} WITH " \
                          "replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;"
        self.session.execute(create_keyspace)

        create_table = f"CREATE TABLE IF NOT EXISTS {self.keyspace}.{self.table} ("

        self.columns = self.get_schema()

        for i, (column, data_type) in enumerate(self.columns):
            if i == 0:
                create_table += f"{column} {to_cql[data_type]} PRIMARY KEY"
            else:
                create_table += f", {column} {to_cql[data_type]}"
        create_table += ");"

        self.session.execute(create_table)

    def insert_data(self):
        insert = f"INSERT INTO {self.keyspace}.{self.table} ("
        insert += ", ".join([name for name, _ in self.columns])
        insert += ") VALUES (" + ", ".join(["?"] * len(self.columns)) + ");"
        insert = self.session.prepare(insert)

        # inserting in chunks of 1000000 rows
        for chunk in pd.read_csv(self.file, sep=self.sep, header=self.header, chunksize=1000000):
            for index, values in chunk.iterrows():
                self.session.execute(insert, values)
