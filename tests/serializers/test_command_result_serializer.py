import json
from infrad.domain import models
from infrad.shared.consts import JobState
from infrad.serializers import command_result_serializer as crs


def test_serialize_domain_command_result():
    command_result = models.CommandResult(
        JobState.COMPLETED, 'message', data={
            'key1': 'value1',
            'key2': 'value2'
        })

    expected_json = """
        {
            "status": 0,
            "message": "message",
            "data": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    """

    assert json.loads(
        json.dumps(command_result,
                   cls=crs.CommandResultEncoder)) == json.loads(expected_json)