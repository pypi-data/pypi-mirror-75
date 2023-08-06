# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Django Framework Adapter
"""

from ..transports.wsgi import WSGITransportCallback


class DjangoFrameworkAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            WSGITransportCallback.from_rule_dict({
                "name": "ecosystem_django_wsgi",
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "test": False,
                "hookpoint": {
                    "klass": "django.core.handlers.wsgi::WSGIHandler",
                    "method": "__call__",
                    "strategy": "wsgi"
                },
                "callbacks": {},
            }, runner, storage)
        ]
