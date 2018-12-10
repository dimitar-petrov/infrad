#! /usr/bin/env python

"""
    File name: screenlock_plugin.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Plugin that manipulates screen locking/unlocking
"""
import logging
from infrad.endpoints.plugin_endpoint import Plugin
from infrad.endpoints.discipline import ScreenLocker
import time

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class SLockPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin used to Lock and Unlock Screen"""
    def __init__(self):
        print("Initialize ScreenLocker Plugin")
        self.slock = ScreenLocker('dpetrov')
        self.module = 'screenlock'

    def do_work(self, action, *args, **kwargs):
        if action == 'mindful_break':
            time.sleep(10)
            self.slock.secure_lock(**kwargs)
            self.slock.unlock()
            return "Success"
        elif action == 'lock':
            self.slock.lock()
            return "Success"
        elif action == 'unlock':
            self.slock.unlock()
            return "Success"

        return "Fail"
