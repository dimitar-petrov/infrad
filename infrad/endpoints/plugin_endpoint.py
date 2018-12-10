#! /usr/bin/env python

"""
    File name: plugin_endpoint.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Base class and executor for plugin architecture of infrad
"""
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from infrad.domain.models import CommandResult
from infrad.shared.consts import JobState

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class Plugin:  # pylint: disable-msg=R0903
    """Base class for all plugins. Singleton instances of subclasses are
    created automatically and stored in Plugin.plugins class field."""
    plugins = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls())

    def do_work(self, action, *args, **kwargs):
        """Actual plugin logic comes her"""
        raise NotImplementedError


class PluginEndpoint:  # pylint: disable=too-few-public-methods
    """Plugin action executor.

    Attributes:
        wait (int, optional): Delay in seconds to wait for action exit status.
    """
    def __init__(self, wait=0):
        self.sync_wait = wait
        self.executor = ThreadPoolExecutor(
            max_workers=5, thread_name_prefix='PLUGIN_EXEC')

    def exec(self, module, action, args, kwargs):
        """Locate the plugin responsible for that action
        and send the needed information for execution

        Args:
        module (str): The module name to be called.
        action (str): Specific action that has to be executed.
        args (list): list of argumets to be passed to the plugin.
        kwargs (dict): Dict of kw args to be passed to the plugin.

        Returns:
        CommandResult: Populated with data from plugin execution.
        """
        for plugin in Plugin.plugins:
            if plugin.module == module:
                print(plugin.do_work, action, args, kwargs)
                future = self.executor.submit(plugin.do_work, action, *args,
                                              **kwargs)
                time.sleep(self.sync_wait)
                if future.done():
                    return CommandResult(JobState.COMPLETED,
                                         'Sync Execution Finished',
                                         future.result())

                return CommandResult(JobState.RUNNING,
                                     'Async Execution In Progress')

        return CommandResult(JobState.FAILED, 'Command not found')
