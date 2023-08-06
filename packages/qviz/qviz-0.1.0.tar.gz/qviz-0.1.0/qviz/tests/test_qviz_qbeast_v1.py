#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Cesare Cugnasco.
# Distributed under the terms of the Modified BSD License.

import ipysheet

from qviz import Qviz, qb1


def test_qviz_creation_blank():
    df = qb1.Source(keyspace='qdb_test', table_name='images')
    w = Qviz(source=df)
    ss = w.selected_sheet.children[0]
    assert isinstance(ss, ipysheet.Sheet)
    w.select_all()
    ss2 = w.selected_sheet.children[0]
    assert ss != ss2
    assert len(w.data.columns) == ss2.columns
    assert Qviz.PAGING_SIZE == ss2.rows
    from IPython.display import display
    display(w)


def test_changing_data_frame():
    df = qb1.Source(keyspace='qdb_test', table_name='images')
    w = Qviz(source=df)
    ss = w.selected_sheet.children[0]
    assert isinstance(ss, ipysheet.Sheet)
    w.select_all()
    ss2 = w.selected_sheet.children[0]
    assert ss != ss2
    assert len(w.data.columns) == ss2.columns
    assert Qviz.PAGING_SIZE == ss2.rows

    df2 = qb1.Source(keyspace='qdb_test', table_name='q2')
    w.source = df2
    ss3 = w.selected_sheet.children[0]
    assert isinstance(ss3, ipysheet.Sheet)
    w.select_all()
    assert len(w.data.columns) == ss3.columns
    assert Qviz.PAGING_SIZE == ss3.rows

    from IPython.display import display
    display(w)


def test_changing_data():
    df = qb1.Source(keyspace='qdb_test', table_name='images')
    w = Qviz(source=df)
    ss = w.selected_sheet.children[0]
    assert isinstance(ss, ipysheet.Sheet)
    w.select_all()
    ss1 = w.selected_sheet.children[0]
    assert ss != ss1
    assert len(w.data.columns) == ss1.columns
    assert Qviz.PAGING_SIZE == ss1.rows
    import pandas as pd
    p = pd.DataFrame(w.data)
    assert not p.empty
    half = ss1.rows // 2
    w._selected = {w.source.URI: w._selected[w.source.URI][:half]}
    ss2 = w.selected_sheet.children[0]
    assert isinstance(ss2, ipysheet.Sheet)
    assert Qviz.PAGING_SIZE // 2 == ss2.rows
    assert half == ss2.rows
    w.select_all()
    ss3 = w.selected_sheet.children[0]
    assert len(w.data.columns) == ss3.columns

    from IPython.display import display
    display(w)
