#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Cesare Cugnasco.
# Distributed under the terms of the Modified BSD License.

from traitlets import HasTraits, List, Tuple, Union, Float, Int, Unicode


class MockSource(HasTraits):
    keyspace = Unicode(allow_none=True).tag(sync=True)
    table_name = Unicode(allow_none=True).tag(sync=True)
    columns = List(trait=Unicode()).tag(sync=True)
    indexed_columns = List(trait=Unicode()).tag(sync=True)
    host = Unicode('localhost').tag(sync=True)
    index_name = Unicode(allow_none=True).tag(sync=False)
    domain = List(trait=Tuple(Union([Float(), Int()]), Union([Float(), Int()])), default_value=[(0, 1), (0, 1), (0, 1)])


def test_query_space():
    from qviz.source import QuerySpace
    a = QuerySpace()
    a.from_point = [1, 2, 3]
    a.to_point = [10, 20, 30]
    b = QuerySpace()
    b.from_point = [2, 3, 4]
    b.to_point = [9, 19, 20]
    assert a.contain(b)
    assert not b.contain(a)


def test_update_domain():
    from qviz.source import QuerySpace
    a = QuerySpace()
    a.from_point = [1, 2, 3]
    a.to_point = [10, 20, 30]
    s = MockSource(domain=[(10, 20), (11, 21), (12, 22)])
    all = a.all_domain(s)
    assert all.from_point == [10, 11, 12]
    assert all.to_point == [20, 21, 22]
    assert all != a
    assert all.precision == a.precision
