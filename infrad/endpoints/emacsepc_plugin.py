#! /usr/bin/env python

"""
    File name: emacsepc_plugin.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Plugin used to control running Emacs process through EPC
"""
import logging
from decouple import config
from epc.client import EPCClient
from infrad.endpoints.plugin_endpoint import Plugin

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class SimpleEPCClient(Plugin):  # pylint: disable-msg=R0903
    """EPC Emacs interface plugin."""
    def __init__(self):
        self.client = EPCClient((config('EPC_SERVER_HOST'),
                                 config('EPC_SERVER_PORT')))
        self.module = 'emacs_control'

    def do_work(self, action, *args, **kwargs):
        response = self.client.call_sync(action, args, timeout=1)
        return response
