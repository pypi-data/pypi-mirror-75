# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Pyramid Framework Adapter
"""

from ..transports.wsgi import WSGITransportCallback


class PyramidFrameworkAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            WSGITransportCallback.from_rule_dict({
                "name": "ecosystem_pyramid_wsgi",
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "test": False,
                "hookpoint": {
                    "klass": "pyramid.router::Router",
                    "method": "__call__",
                    "strategy": "wsgi"
                },
                "callbacks": {},
            }, runner, storage)
        ]
