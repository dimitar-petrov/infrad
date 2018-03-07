#! /usr/bin/env python

"""
    File name: core.py
    Author: Dimitar Petrov
    Date created: 2018/03/03
    Python Version: 3.6
    Description: Core functionality of infrad
"""
import time
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
import zmq
from decouple import config
from infrad.events import ResponseEvent, EVENT_TYPE
from infrad.plugin import Plugin
from infrad.utils import GracefulInterruptHandler

class ZMQListener(Thread):
    """ZMQ Server responsible for handling events from multiple sources"""
    def __init__(self):
        super().__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:{}".format(config('ZMQ_SERVER_PORT')))
        self.timeout = 10
        self.stop_request = Event()
        self.executor = ThreadPoolExecutor(
            max_workers=9, thread_name_prefix='PLUGIN_EXEC')

    def run(self):
        while not self.stop_request.isSet():
            try:
                request = self.socket.recv_pyobj(zmq.NOBLOCK)
            except zmq.Again:
                continue
            else:
                if request.type == EVENT_TYPE.REQUEST:
                    return_value = self._handle_command(request)
                    self.socket.send_pyobj(
                        ResponseEvent('Response to {} is: {}'.format(
                            request.method, return_value)))

    def _handle_command(self, request):
        for plugin in Plugin.plugins:
            if plugin.init_command == request.method:
                future = self.executor.submit(plugin.do_work, **request.kwargs)
                if future.done():
                    return future.result()
                if request.sync:
                    return self._wait_for_future_result(future)
                return "Async Execution in ThreadPool"

        return "Method not found {}".format(request.method)

    @staticmethod
    def _wait_for_future_result(future, retries=10):
        for _ in range(retries):
            if future.done():
                return future.result()
            time.sleep(1)
        return "Timeout"

    def join(self, timeout=None):
        self.stop_request.set()
        super().join(timeout)

def main():
    """Start the listener and wait for SIGTERM or SIGINT signal"""

    listener = ZMQListener()
    listener.start()

    with GracefulInterruptHandler() as han:
        while True:
            time.sleep(1)
            if han.interrupted:
                break

    listener.join()

if __name__ == '__main__':
    main()
