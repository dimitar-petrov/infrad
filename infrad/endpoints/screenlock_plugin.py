from infrad.endpoints.plugin_endpoint import Plugin
from infrad.discipline import ScreenLocker


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
