#! /usr/bin/env python

"""
    File name: zmqclient.py
    Author: Dimitar Petrov
    Date created: 2018/03/03
    Python Version: 3.6
    Description: ZeroMQ client
"""
import zmq
from decouple import config

class ZMQSender: #pylint: disable-msg=R0903
    """ZMQ Client used to send events"""
    def __init__(self):
        context = zmq.Context()
        print("Connecting to server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:{}".format(config('ZMQ_SERVER_PORT')))

    def send_request(self, request):
        """Forward request to ZMQListener and return the response"""
        print("Sending request: {}".format(request))
        self.socket.send_pyobj(request)
        # response = self._response_wait()
        response = self.socket.recv_pyobj()
        print("Reply to {} is {}".format(request, response))
        return response
