#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Cesare Cugnasco.
# Distributed under the terms of the Modified BSD License.

"""
This files contains all the widgets that keep information over a collection of data.
"""

from abc import abstractmethod

import ipysheet
import pandas as pd
from ipywidgets import Widget, DOMWidget, widget_serialization, register, Output, Button, HBox, VBox, Dropdown
from traitlets import (Int, Unicode, List, Instance, observe, Dict, Float, Union, Tuple, HasTraits)
from ipysheet.pandas_loader import from_dataframe
from qviz import log
from qviz.model import QuerySpace
from ._frontend import module_name, module_version


class Metadata(HasTraits, dict):
    """
    Generic Source metadata holder.
      """
    columns = List(trait=Unicode(), minlen=1).tag(sync=True)
    indexed_columns = List(trait=Unicode()).tag(sync=True)
    index_name = Unicode(allow_none=True).tag(sync=False)
    domain = List(trait=Tuple(Union([Float(), Int()]), Union([Float(), Int()])),
                  default_value=[(0, 1), (0, 1), (0, 1)], minlen=1).tag(sync=True)

    def __init__(self, *args, **kwargs):
        HasTraits.__init__(self, *args, **kwargs)
        dict.__init__(self, self.__dict__['_trait_values'])


@register
class Source(Widget):
    """
    A DataFrame represents a high-level, table-like collection of data. It is compatible
    with a DataFrame from Pandas', Spark's, or Apache Arrow's DataFrame
      """
    _model_name = Unicode('SourceModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    URI = Unicode(allow_none=True).tag(sync=True)
    metadata = Instance(Metadata, allow_none=True, default_value=None).tag(sync=True)

    @abstractmethod
    def query(self, query_space: QuerySpace) -> pd.DataFrame:
        pass

    @abstractmethod
    def same_source(self, other) -> bool:
        pass


numerics_dtypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']


@register
class Qviz(DOMWidget):
    """
    A DOMWidget that allows to explore a DataFrame as a table.
    """
    PAGING_SIZE = 20
    _model_name = Unicode('QvizModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('QvizView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    source = Instance(Source).tag(sync=True, **widget_serialization)
    query_space = Instance(QuerySpace, allow_none=False).tag(sync=True, **widget_serialization)
    _selected = Dict(List(default_value=[])).tag(sync=True)
    data = Instance(pd.DataFrame, allow_none=True, default_value=pd.DataFrame()).tag(sync=False)
    # TODO this is a temporal workaround, the idea is to move to a binary transport layer or at lest
    # asinch comms (https://jupyter-notebook.readthedocs.io/en/stable/comms.html)
    frontend_data = Dict().tag(sync=True)

    def __init__(self, query_space=QuerySpace(), **kwargs):
        """
        Creates a Table widget for the input source
        """
        super().__init__(query_space=query_space, **kwargs)
        self.selected_sheet = VBox([ipysheet.sheet()])

        def _update_source(change):
            if self.source.metadata is not None:
                with log:
                    print("Qviz' s metadata changed ", self.source.metadata)
                self.query_space = self.query_space.all_domain(self.source.metadata)

        self.source.observe(_update_source, names="metadata")

        _update_source(None)

    @property
    def selected(self):
        if self.source.URI in self._selected:
            return self.data.loc[self.data.index.intersection(self._selected[self.source.URI])]
        else:
            return pd.DataFrame()

    @observe("query_space")
    def _filter__space(self, change):
        if not self.query_space.empty:
            with log:
                print("Updating query space")
            if self.source.is_valid():
                self.data = self.source.query(self.query_space)

    @observe('data')
    def updated_data(self, change):
        if not self.data.empty:
            self.frontend_data = self.data.select_dtypes(include=numerics_dtypes).to_dict(orient="split")

    @observe('_selected')
    def _update_sheet(self, change):
        with log:
            print("changed SELECTED: updating ", self.source.URI)
        if self.source.URI in self._selected:
            sheet = from_dataframe(self.selected.head(Qviz.PAGING_SIZE))
            from IPython.display import FileLink

            link = Output()
            file_type = Dropdown(
                value='csv',
                placeholder='Choose Someone',
                options=['csv', 'xls', 'parquet', 'feather'],
                description='File format:',
                disabled=False
            )
            conversions = {
                'csv': lambda f: self.selected.to_csv(f, index=False),
                'xls': lambda f: self.selected.to_excel(f, index=False),
                'parquet': lambda f: self.selected.to_parquet(f, index=False),
                'feather': lambda f: self.selected.to_feather(f)
            }

            def generate_file(a):
                import time
                ts = time.gmtime()
                f = "./" + time.strftime("%Y-%m-%d--%H-%M-%S", ts) + "." + file_type.value
                conversions[file_type.value](f)
                link.clear_output()
                with link:
                    from IPython.core.display import display
                    display(FileLink(f))

            download_buttom = Button(
                description="Generate file",
                buttom_style='success',
                icon='download')
            download_buttom.on_click(generate_file)

            for c in sheet.cells:
                c.read_only = True

            self.selected_sheet.children = [sheet, HBox([file_type, download_buttom, link])]
        else:
            self.selected_sheet.children = [ipysheet.sheet()]

    def select_all(self):
        self._selected = {self.source.URI: list(self.data.index)}
