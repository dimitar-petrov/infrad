#! /usr/bin/env python

"""
    File name: utils.py
    Author: Dimitar Petrov
    Date created: 2018/03/07
    Python Version: 3.6
    Description: Utilities for infrad
"""

import signal

class GracefulInterruptHandler:
    """Context manager for capturing signals"""
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig
        self.interrupted = False
        self.released = False
        self.original_handler = signal.getsignal(self.sig)

    def __enter__(self):
        def handler(signum, frame):
            """Actual signal handler"""
            print('Captured signal [{}] from line [{}]'. format(
                signum, frame.f_lineno))
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        """Release the context manager"""
        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)
        self.released = True

        return True
