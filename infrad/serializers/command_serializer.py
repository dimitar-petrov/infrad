import json


class CommandEncoder(json.JSONEncoder):
    """Specific Encoder for Command"""
    def default(self, o):  # pylint: disable=E0202
        try:
            to_serialize = {
                'comm': o.comm,
                'args': o.args,
                'kwargs': o.kwargs,
                'sync': o.sync,
            }

            return to_serialize
        except AttributeError:
            return super().default(o)
