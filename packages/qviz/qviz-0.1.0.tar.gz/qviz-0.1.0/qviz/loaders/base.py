from abc import ABC, abstractmethod
from typing import List

import pandas as pd

supported_backends = ["Cassandra"]


class Loader(ABC):

    def __init__(self, file: str, sep: str = ",", header: str = "infer", nrows: int = 100):
        self.file = file
        self.sep = sep
        self.header = header
        self.nrows = nrows
        self.type = self.file.split(".")[-1]

    @abstractmethod
    def create_schema(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def insert_data(self) -> None:
        pass

    def get_schema(self):
        if self.type == "csv":
            df = pd.read_csv(self.file, sep=self.sep, header=self.header, nrows=self.nrows)
        else:
            raise Exception(f"File type {self.type} not yet implemented.")

        if self.header == "infer":
            columns = df.columns
        else:
            columns = ["column" + str(i) for i in range(len(df.columns))]

        return [(column, t.name) for column, t in zip(columns, df.dtypes)]
