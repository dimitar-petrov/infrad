import time
import logging
from concurrent.futures import ThreadPoolExecutor
from infrad.domain.models import CommandResult
from infrad.shared.consts import JobState

logger = logging.getLogger(__name__)


class Plugin:  # pylint: disable-msg=R0903
    """Base class for all plugins. Singleton instances of subclasses are
    created automatically and stored in Plugin.plugins class field."""
    plugins = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls())

    def do_work(self, *args, **kwargs):
        """Actual plugin logic comes her"""
        raise NotImplementedError


class PluginEndpoint:
    def __init__(self, wait=1):
        self.sync_wait = wait
        self.executor = ThreadPoolExecutor(
            max_workers=5, thread_name_prefix='PLUGIN_EXEC')

    def exec(self, module, action, args, kwargs, sync=False):
        for plugin in Plugin.plugins:
            if plugin.module == module:
                future = self.executor.submit(plugin.do_work, action, *args,
                                              **kwargs)
                time.sleep(self.sync_wait)
                if future.done():
                    return CommandResult(JobState.COMPLETED,
                                         'Sync Execution Finished',
                                         future.result())
                else:
                    return CommandResult(JobState.RUNNING,
                                         'Async Execution In Progress')
        return CommandResult(JobState.FAILED, 'Command not found')
