#!/usr/bin/env python
# coding: utf-8

# Copyright (c) wangsijie.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Any
from ._frontend import module_name, module_version


class QuizWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('QuizModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('QuizView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Any([]).tag(sync=True)
    quiz_id = Unicode('').tag(sync=True)
    def __init__(self, value, quiz_id):
        DOMWidget.__init__(self)
        self.value = value
        self.quiz_id = quiz_id
