import json


class CommandEncoder(json.JSONEncoder):
    """Specific Encoder for Command"""
    def default(self, o):  # pylint: disable=E0202
        try:
            to_serialize = {
                'module': o.module,
                'action': o.action,
                'args': o.args,
                'kwargs': o.kwargs,
                'sync': o.sync,
            }

            return to_serialize
        except AttributeError:
            return super().default(o)
