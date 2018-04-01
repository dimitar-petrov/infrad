import pytest

from infrad.use_cases import request_objects as ro


def test_build_command_execute_request_object():
    req = ro.CommandExecuteRequestObject('command', ['arg1', 'arg2'], {
        'kwarg1': 'value1',
        'kwarg2': 'value2'
    })

    assert bool(req) is True
    assert req.comm == 'command'
    assert req.args == ['arg1', 'arg2']
    assert req.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}
    assert req.sync is False


def test_build_command_execute_request_object_from_dict():
    req = ro.CommandExecuteRequestObject.from_dict({
        'comm': 'command',
        'args': ['arg1', 'arg2'],
        'kwargs': {
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        },
        'sync': True
    })

    assert req.comm == 'command'
    assert req.args == ['arg1', 'arg2']
    assert req.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}
    assert req.sync is True


def test_build_command_execute_request_object_from_dict_with_invalid_args():
    req = ro.CommandExecuteRequestObject.from_dict({
        'comm': 'command',
        'args': 'args',
        'kwargs': {
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        },
        'sync': True
    })

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'args'
    assert bool(req) is False
