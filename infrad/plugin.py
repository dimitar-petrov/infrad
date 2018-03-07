#! /usr/bin/env python

"""
    File name: plugin.py
    Author: Dimitar Petrov
    Date created: 2018/03/03
    Python Version: 3.6
    Description: Plugin Infrastructure
"""

from infrad.discipline import ScreenLocker

class Plugin: #pylint: disable-msg=R0903
    """Base class for all plugins. Singleton instances of subclasses are
    created automatically and stored in Plugin.plugins class field."""
    plugins = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls())

    def do_work(self, **kwargs):
        """Actual plugin logic comes her"""
        raise NotImplementedError

class SLockPlugin(Plugin): #pylint: disable-msg=R0903
    """Plugin used to Lock and Unlock Screen"""
    def __init__(self):
        print("Initialize ScreenLocker Plugin")
        self.slock = ScreenLocker('dpetrov')
        self.init_command = 'screenlock'

    def do_work(self, **kwargs):
        self.slock.secure_lock(**kwargs)
        self.slock.unlock()
        return "Success"

class TestDelay(Plugin): #pylint: disable-msg=R0903
    """Test plugin to compare sync vs async execution"""
    def __init__(self):
        print("Initialize Test Delay Plugin")
        self.init_command = 'test'

    def do_work(self, **kwargs):
        import time
        delay = kwargs.get('delay', 0)
        print('Waiting for: {}'.format(delay))
        time.sleep(int(delay))
        return "Success"
