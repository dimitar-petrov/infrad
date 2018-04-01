from infrad.domain import models as m


def test_command_result_init():
    result = m.CommandResult(
        0, 'message', data={
            'key1': 'value1',
            'key2': 'value2'
        })

    assert result.status == 0
    assert result.message == 'message'
    assert result.data == {'key1': 'value1', 'key2': 'value2'}


def test_command_result_from_dict():
    result = m.CommandResult.from_dict({
        'status': 0,
        'message': 'message',
        'data': {
            'key1': 'value1',
            'key2': 'value2'
        }
    })

    assert result.status == 0
    assert result.message == 'message'
    assert result.data == {'key1': 'value1', 'key2': 'value2'}
