# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#

from .django import DjangoFrameworkAdapter
from .flask import FlaskFrameworkAdapter
from .pyramid import PyramidFrameworkAdapter


def init(interface_manager):
    """ Sqreen ecosystem framework adapters initialization
    """
    interface_manager.register(DjangoFrameworkAdapter())
    interface_manager.register(FlaskFrameworkAdapter())
    interface_manager.register(PyramidFrameworkAdapter())
