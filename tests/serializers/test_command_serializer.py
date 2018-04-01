import json
from infrad.domain import models
from infrad.serializers import command_serializer as cs


def test_serialize_domain_command():
    command = models.Command(
        'command',
        args=['arg1', 'arg2'],
        kwargs={
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        },
        sync=True)

    expected_json = """
        {
            "comm": "command",
            "args": ["arg1", "arg2"],
            "kwargs": {
                "kwarg1": "value1",
                "kwarg2": "value2"
            },
            "sync": true
        }
    """

    assert json.loads(json.dumps(
        command, cls=cs.CommandEncoder)) == json.loads(expected_json)
