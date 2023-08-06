#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Cesare Cugnasco.
# Distributed under the terms of the Modified BSD License.
import re

import qviz.sources.qbeast_v1 as qb1
from qviz.source import Metadata


def test_source():
    source = qb1.Source(keyspace='qdb_test',
                        table_name='images')
    m = source.metadata
    assert set(m.columns) == {"img_id", "confidence", "img_url", "source", "t", "x", "y", "z"}
    assert m.index_name == 'images_idx'
    assert set(m.indexed_columns) == {'x', 'y', 'z'}
    assert m.domain == [(0, 10), (0, 10), (0, 10)]


def test_source_changes():
    s = qb1.Source(keyspace='qdb_test',
                   table_name='images')
    m = s.metadata
    assert set(m.columns) == {"img_id", "confidence", "img_url", "source", "t", "x", "y", "z"}
    assert m.index_name == 'images_idx'
    assert set(m.indexed_columns) == {'x', 'y', 'z'}
    assert m.domain == [(0, 10), (0, 10), (0, 10)]

    s.table_name = 'q2'
    m2 = s.metadata
    assert m2 != m
    assert set(m2.columns) == {"img_id", "img_url", "t", "x", "y", "z"}
    assert m2.index_name == 'iq2'
    assert set(m2.indexed_columns) == {'x', 'y', 'z'}
    assert m2.domain == [(0, 10), (0, 10), (0, 10)]


def test_predicate_query_space():
    from qviz.source import QuerySpace
    a = QuerySpace(precision=0.2,
                   limit=12)
    a.from_point = [1, 2, 3]
    a.to_point = [10, 20, 30]
    source = qb1.Source(
        keyspace="ks",
        table_name="tab",
        metadata=Metadata(
            columns=["a", "b", "c", "d", "e"],
            indexed_columns=["a", "c", "e"],
            domain=[(0, 1)],
            index_name="ciao"
        ),
        _skip_set_up=True
    )
    q = source.select_predicate(a)

    regex = "SELECT \\* FROM ks.tab WHERE a >= 1.0 AND c >= 2.0 AND e >= 3.0 AND a < 10.0 AND c < 20.0 AND e < 30.0"
    regex = regex + f" AND expr\\(ciao,'precision=0.2,limit=12:[0-9]+'\\) LIMIT 2147483647 ALLOW FILTERING"
    regex = re.compile(regex)
    assert regex.match(q) is not None


def test_predicate_no_index():
    from qviz.source import QuerySpace
    a = QuerySpace(precision=0.2,
                   limit=12)
    a.from_point = [1, 2, 3]
    a.to_point = [10, 20, 30]
    source = qb1.Source(
        keyspace="ks",
        table_name="tab",
        metadata=Metadata(
            columns=["a", "b", "c", "d", "e"],
            indexed_columns=[],
            index_name=None,
        ),
        _skip_set_up=True
    )
    q = source.select_predicate(a)
    regex = re.compile(f"SELECT \\* FROM ks.tab LIMIT 12")
    assert regex.match(q) is not None
