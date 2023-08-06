# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Signal Client API
"""
import logging

from ._vendors.sqreen_security_signal_sdk import Client
from .config import CONFIG
from .http_client import USER_AGENT

LOGGER = logging.getLogger(__name__)


class SignalClient(Client):

    user_agent = USER_AGENT


def get_signal_client(session, batch_size=0, max_staleness=0,
                      user_agent=None):
    """ Get a Signal Client.
    """
    if session.use_legacy_url:
        LOGGER.debug("Using legacy URL for signal ingestion")
        url = CONFIG["LEGACY_URL"]
    else:
        LOGGER.debug("Using new URL for signal ingestion")
        url = CONFIG["INGESTION_URL"]
    if user_agent is not None:
        SignalClient.user_agent = user_agent
    client = SignalClient(
        token=session.session_token,
        max_batch_size=batch_size,
        interval_batch=max_staleness,
        session_token=True,
        proxy_url=CONFIG["PROXY_URL"],
        base_url=url,
    )
    return client
