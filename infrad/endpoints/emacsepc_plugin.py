import logging
from decouple import config
from epc.client import EPCClient
from infrad.endpoints.plugin_endpoint import Plugin

logger = logging.getLogger(__name__)


class SimpleEPCClient(Plugin):
    def __init__(self):
        self.client = EPCClient((config('EPC_SERVER_HOST'),
                                 config('EPC_SERVER_PORT')))
        self.init_command = 'emacs_control'

    def do_work(self, *args, **kwargs):
        action = kwargs.get('action')
        if action is not None:
            return self.client.call_sync(action, args, timeout=1)
        else:
            return "Failed: Supply action"
