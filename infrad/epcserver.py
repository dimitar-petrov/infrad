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

class SimpleEPCServer(object):

    def __init__(self):
        self.setup_epc()

    def setup_epc(self):
        self.server = ThreadingEPCServer(
            ('localhost', int(config('EPC_SERVER_PORT'))), log_traceback=True)
        self.zmqc = ZMQSender()

        # Setup logger
        self.server.logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(filename='python-epc.log', mode='w')
        ch.setLevel(logging.DEBUG)
        self.server.logger.addHandler(ch)

        # Setup server thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.allow_reuse_address = True

        self.server.register_function(self.command)

    def command(self, method, args=None, sync=True):
        kwargs = dict([x.split(':') for x in args])
        response = self._forward_request(
            RequestEvent(method, kwargs, sync=sync))

        self._respond(response)

    def _forward_request(self, request):
        self.server.logger.info(request)
        response = self.zmqc.send_request(request)
        return response

    def _respond(self, response):
        handler = self.server.clients[0]
        handler.call('message', [response.text])

    def destroy(self):
        self.server.shutdown()

    def main(self):
        self.server_thread.start()

if __name__ == "__main__":
    server = SimpleEPCServer()
    server.main()
