import json


class CommandResultEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        try:
            to_serialize = {
                'status': o.status,
                'message': o.message,
                'data': o.data,
            }

            return to_serialize
        except AttributeError:
            return super().default(o)
