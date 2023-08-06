# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
from ....constants import ACTIONS
from ....rules import RuleCallback
from ....workflow import Transport


class HttpClientTransportCallback(RuleCallback):

    def pre(self, instance, args, kwargs, **options):
        try:
            host_ip, host_port = instance.sock.getpeername()
        except Exception:
            host_ip, host_port = None, None

        transport = Transport({
            "type": "http",
            "host": instance.host or host_ip,
            "host_ip": host_ip,
            "host_port": host_port,
        })

        context = self.runner.interface_manager.call("context")
        if not self.runner.interface_manager.call("new_data_out_pre", context, transport):
            return

        tracing_identifier = transport.get("tracing_identifier")
        if tracing_identifier is None:
            return

        new_args = list(args)
        new_headers = new_args[3] = dict(args[3])
        new_headers["X-Sqreen-Trace-Identifier"] = tracing_identifier
        return {
            "status": ACTIONS["MODIFY_ARGS"],
            "args": (new_args, kwargs),
        }


class HttpClientTransportAdapter:

    def instrumentation_callbacks(self, runner, storage):
        return [
            HttpClientTransportCallback.from_rule_dict({
                "name": "ecosystem_http_client",
                "rulespack_id": "ecosystem/transport",
                "block": True,
                "test": False,
                "hookpoint": {
                    "klass": "http.client::HTTPConnection",
                    "method": "_send_request"
                },
                "callbacks": {},
            }, runner, storage)
        ]
