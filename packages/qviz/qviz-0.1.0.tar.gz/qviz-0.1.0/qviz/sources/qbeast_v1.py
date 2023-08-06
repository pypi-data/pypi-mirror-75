import re
from functools import lru_cache
from random import getrandbits

import pandas as pd
from cassandra.cluster import Cluster, Session
from cassandra.policies import TokenAwarePolicy, DCAwareRoundRobinPolicy
from ipywidgets import register, HBox, Dropdown
from traitlets import Unicode, List, observe, Bool

import qviz
from qviz import log
from qviz.source import Metadata
from .._frontend import module_name, module_version
from ..model import QuerySpace


@lru_cache()
def __gs(cp):
    c = Cluster(contact_points=[cp], load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy()))
    return c.connect()


def get_session(host: str = None) -> Session:
    if host is None:
        import os
        cp = os.environ.get('CONTACT_NAMES', 'localhost').split(",")[0]
    else:
        cp = host
    return __gs(cp)


@register
class Source(qviz.Source):
    """
    Qbeast source implementation.
      """
    _model_name = Unicode('SourceModel').tag(sync=True)  # We use the same model of the common source
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    keyspace = Unicode(allow_none=True)
    table_name = Unicode(allow_none=True)
    host = Unicode('localhost').tag(sync=True)
    _skip_set_up = Bool(default_value=False).tag(sync=False)

    def __init__(self, **kwargs):
        super(Source, self).__init__(**kwargs)

    def _set_up_index(self):
        if self._skip_set_up:
            return

        with log:
            print("QbeastV1 Source: download indexed metadata")

        with self.hold_trait_notifications():

            columns = [p.column_name for p in self.session.execute(
                " SELECT column_name FROM system_schema.columns  WHERE keyspace_name=%s and table_name=%s",
                [self.keyspace, self.table_name]
            )]
            q = self.session.execute(
                "SELECT index_name, options FROM system_schema.indexes WHERE keyspace_name= %s "
                "AND table_name= %s AND kind='CUSTOM' AND "
                "options CONTAINS 'es.bsc.qbeast.index.QbeastIndex'  ALLOW FILTERING ",
                [self.keyspace, self.table_name]).one()

            if q is None:
                with log:
                    print("WARN: I cannot find  a Qbeast index on {}.{}".format(self.keyspace, self.table_name))
                index_name, indexed_columns, domain = None, [], []
            else:
                index_name, options = q
                indexed_columns = options['target'].split(", ")
                t = re.search(r".*Transformation\((?P<domain>(?:\(-?[0-9.]+,-?[0-9.]+\),?){3})\)",
                              options['transformation'])
                domain = []
                if t != None:
                    domain = [tuple([float(f), float(t)]) for f, t in
                              map(lambda a: re.search(r"\(?(-?[0-9.]+),(-?[0-9.]+)\)?", a).groups(),
                                  t.group('domain').split("),("))]

            self.metadata = Metadata(
                columns=columns,
                index_name=index_name,
                indexed_columns=indexed_columns,
                domain=domain
            )

    @observe("table_name")
    def _change_table_name(self, change):
        with log:
            print("QbeastV1 source: updating table_name")
        with self.hold_trait_notifications():
            self.URI = f"qb1://{self.host}/{self.keyspace}.{self.table_name}"
            self._set_up_index()

    def query(self, query_space: QuerySpace) -> pd.DataFrame:
        return pd.DataFrame(self.session.execute(self.select_predicate(query_space)))

    def select_predicate(self, query_space: QuerySpace):

        if self.metadata.index_name is not None:
            froms = map(lambda a: "%s >= %s" % a, zip(self.metadata.indexed_columns, query_space.from_point))
            tos = map(lambda a: "%s < %s" % a, zip(self.metadata.indexed_columns, query_space.to_point))
            predicates = list(froms) + list(tos)

            return f"SELECT * FROM {self.keyspace}.{self.table_name} WHERE " + (" AND ".join(predicates)) + \
                   f" AND expr({self.metadata.index_name},'precision={query_space.precision}," + \
                   f"limit={query_space.limit}:{getrandbits(32)}')" \
                   " LIMIT 2147483647 ALLOW FILTERING"
        else:
            return f"SELECT * FROM {self.keyspace}.{self.table_name} LIMIT {query_space.limit}"

    @property
    def session(self) -> Session:
        return get_session(self.host)

    def is_valid(self) -> bool:
        return self.keyspace != None and self.keyspace != '' and \
               self.table_name != None and self.table_name != '' and \
               self.host != None and self.host != ''

    def same_source(self, other) -> bool:
        return type(other) == Source and self.keyspace == other.keyspace and self.table_name == other.table_name


@register
class SourceSelector(HBox, Source):
    """
    Graphical widget to pick a table.
    Note, this Widget used the HBoxModel and HBoxView.
    """
    keyspaces = List(Unicode()).tag(sync=True)
    tables = List(Unicode(), default_value=[]).tag(sync=True)

    def __init__(self, **kwargs):
        """
        Utility widget that allows to pick a keyspace and a table
        """
        super().__init__(skip_init=True, **kwargs)

        session = get_session(self.host)

        ksps = list(filter(lambda a: not a.startswith("system_"),
                           map(lambda x: x.keyspace_name,
                               session.execute("SELECT keyspace_name FROM system_schema.keyspaces "))))
        self.key_drop = Dropdown(
            options=ksps,
            description='Keyspace:',
            value=None,
            disabled=False,
        )
        self.table_drop = Dropdown(
            options=[],
            description='Table:',
            disabled=False,
        )

        self.children = [self.key_drop, self.table_drop]

        def update_tab_list(change):
            self.table_drop.value = None
            tables = list(map(lambda x: x.table_name,
                              get_session(self.host).execute(
                                  "SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s",
                                  [change['new']])))
            self.table_drop.options = [""] + tables

        self.key_drop.observe(update_tab_list, "value")

        def update_table(change):
            if change['new'] != "" and change['new'] is not None:
                with self.hold_trait_notifications():
                    self.keyspace = self.key_drop.value
                    self.table_name = change['new']

        self.table_drop.observe(update_table, "value")
