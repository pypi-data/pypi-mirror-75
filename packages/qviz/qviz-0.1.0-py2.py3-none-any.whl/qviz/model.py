import pandas as pd
import pyarrow as pa
from ipywidgets import Widget
from traitlets import (Int, List, Float, Union, Unicode)

from ._frontend import module_name, module_version


class QuerySpace(Widget):
    _model_name = Unicode('QuerySpaceModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    from_point = List(trait=Union([Float(), Int()]), default_value=[])
    to_point = List(trait=Union([Float(), Int()]), default_value=[])
    precision = Float(min=0, max=1, default_value=0.1)
    limit = Int(min=1, default_value=100)

    def contain(self, other):
        return self.precision >= other.precision and sum(
            map(lambda a: a[0] <= a[1], zip(self.from_point, other.from_point))) == \
               sum(map(lambda a: a[0] >= a[1], zip(self.to_point, other.to_point))) == len(self.from_point)

    def all_domain(self, metadata):
        new_self = QuerySpace(
            from_point=[],
            to_point=[],
            precision=self.precision,
            limit=self.limit
        )
        with self.hold_trait_notifications():
            for f, t in metadata.domain:
                new_self.from_point.append(f)
                new_self.to_point.append(t)
        return new_self

    @property
    def empty(self):
        return len(self.from_point) is 0 or len(self.to_point) is 0


def _arrow_to_json(x: pa.Table, obj):
    return x.to_pydict()


def _json_to_widget(x, obj):
    return


arrow_serialization = {
    'from_json': _json_to_widget,
    'to_json': _arrow_to_json
}


def _panda_to_json(x, obj):
    if x is None:
        return {}
    return x.to_json()


def _json_to_panda(x, obj):
    return pd.read_json(x)


panda_serialization = {
    'from_json': pd.read_json,
    'to_json': _panda_to_json
}