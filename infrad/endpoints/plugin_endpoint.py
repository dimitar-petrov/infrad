from concurrent.futures import ThreadPoolExecutor
from infrad.plugin import Plugin
from infrad.domain.models import CommandResult
from infrad.shared.consts import JOB_STATE


class PluginEndpoint:
    def __init__(self):
        self.executor = ThreadPoolExecutor(
            max_workers=5, thread_name_prefix='PLUGIN_EXEC')

    def exec(self, command, args, kwargs, sync=False):
        for plugin in Plugin.plugins:
            if plugin.init_command == command:
                future = self.executor.submit(plugin.do_work, *args, **kwargs)
                if future.done():
                    return CommandResult(JOB_STATE.COMPLETED, 'Sync Execution Finished', future.result())
                else:
                    return CommandResult(JOB_STATE.RUNNING, 'Async Execution In Progress')
        return CommandResult(JOB_STATE.FAILED, 'Command not found')

