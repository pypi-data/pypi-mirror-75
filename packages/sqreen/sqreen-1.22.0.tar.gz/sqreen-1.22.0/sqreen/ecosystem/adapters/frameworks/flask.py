# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Flask Framework Adapter
"""

from ..transports.wsgi import WSGITransportCallback


class FlaskFrameworkAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            WSGITransportCallback.from_rule_dict({
                "name": "ecosystem_flask_wsgi",
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "test": False,
                "hookpoint": {
                    "klass": "flask::Flask",
                    "method": "__call__",
                    "strategy": "wsgi",
                },
                "callbacks": {},
            }, runner, storage)
        ]
