#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Cesare Cugnasco.
# Distributed under the terms of the Modified BSD License.
from ipywidgets import Output

log = Output()

from ._version import __version__, version_info

from .nbextension import _jupyter_nbextension_paths

from .source import Source, Qviz
import qviz.sources.qbeast_v1 as qb1
