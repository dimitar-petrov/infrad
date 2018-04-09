import logging
from infrad.endpoints.plugin_endpoint import Plugin
from infrad.discipline import ScreenLocker

logger = logging.getLogger(__name__)


class SLockPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin used to Lock and Unlock Screen"""
    def __init__(self):
        print("Initialize ScreenLocker Plugin")
        self.slock = ScreenLocker('dpetrov')
        self.module = 'screenlock'

    def do_work(self, action, **kwargs):
        if action == 'mindful_break':
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
