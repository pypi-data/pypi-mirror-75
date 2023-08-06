# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
import sys

from ....rules import RuleCallback
from ....workflow import Transport

if sys.version_info[0] >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


class BotocoreTransportCallback(RuleCallback):

    FILTERED_OPERATIONS = {
        "kinesis": {
            "PutRecord": "out",
            "PutRecords": "out",
            "GetRecords": "in",
        },
        "sqs": {
            "SendMessage": "out",
            "SendMessageBatch": "out",
            "ReceiveMessage": "in",
        },
    }

    def pre(self, instance, args, kwargs, **options):
        endpoint_prefix = getattr(instance, "_endpoint_prefix", None)
        operations = self.FILTERED_OPERATIONS.get(endpoint_prefix)
        if operations is None:
            return
        operation_model = args[0]
        op = operations.get(operation_model.name)
        if op is None:
            return

        try:
            host = urlparse.urlparse(instance.host).netloc
            if ":" in host:
                host, port = host.split(":", 1)
            else:
                port = None
        except Exception:
            host, port = None, None

        transport = Transport({
            "type": "aws-{}".format(endpoint_prefix),
            "host": host,
            "host_port": port,
        })

        context = self.runner.interface_manager.call("context")
        self.runner.interface_manager.call("new_message_{}_pre".format(op), context, transport)


class BotocoreTransportAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            BotocoreTransportCallback.from_rule_dict({
                "name": "ecosystem_botocore",
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "test": False,
                "hookpoint": {
                    "klass": "botocore.endpoint::Endpoint",
                    "method": "make_request",
                },
                "callbacks": {},
            }, runner, storage)
        ]
