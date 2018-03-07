#! /usr/bin/env python

"""
    File name: epcserver.py
    Author: Dimitar Petrov
    Date created: 2018/03/04
    Python Version: 3.6
    Description: EPCS Server that is managing the communication with emacs
"""
import threading
import logging

from epc.server import ThreadingEPCServer
from decouple import config
from infrad.zmqclient import ZMQSender
from infrad.events import RequestEvent

class SimpleEPCServer:
    """Two way communication with emacs through EPC"""

    def __init__(self):
        self.setup_epc()

    def setup_epc(self):
        """Start the EPC epc_server in a separate thread"""
        self.epc_server = ThreadingEPCServer(
            ('localhost', int(config('EPC_SERVER_PORT'))), log_traceback=True)
        self.zmqc = ZMQSender()

        # Setup logger
        self.epc_server.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(filename='python-epc.log', mode='w')
        file_handler.setLevel(logging.DEBUG)
        self.epc_server.logger.addHandler(file_handler)

        # Setup epc_server thread
        self.server_thread = threading.Thread(target=self.epc_server.serve_forever)
        self.server_thread.allow_reuse_address = True

        self.epc_server.register_function(self.command)

    def command(self, method, args=None, sync=True):
        """Process a command received from emacs"""
        kwargs = dict([x.split(':') for x in args])
        response = self._forward_request(
            RequestEvent(method, kwargs, sync=sync))

        self._respond(response)

    def _forward_request(self, request):
        """Forward the request to the core app"""
        self.epc_server.logger.info(request)
        response = self.zmqc.send_request(request)
        return response

    def _respond(self, response):
        """Return the response from core app back to emacs"""
        handler = self.epc_server.clients[0]
        handler.call('message', [response.text])

    def destroy(self):
        """Stop the epc server"""
        self.epc_server.shutdown()

    def main(self):
        """Main function to start EPC server"""
        self.server_thread.start()

if __name__ == "__main__":
    epc_server = SimpleEPCServer()
    epc_server.main()
