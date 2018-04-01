import pytest

from infrad.domain import models
from infrad.shared import response_object as res
from infrad.use_cases import request_objects as req
from infrad.use_cases import command_execute_use_case as uc


@pytest.fixture
def domain_command_requests():
    command1 = {
        'comm': 'command1',
        'args': ['arg11', 'arg12', 'arg13'],
        'kwargs': {
            'kwarg11': 'value11',
            'kwarg12': 'value12'
        },
        'sync': True
    }

    command2 = {
        'comm': 'command2',
        'args': ['arg21', 'arg22', 'arg23'],
        'kwargs': {
            'kwarg21': 'value21',
            'kwarg22': 'value22'
        },
        'sync': True
    }

    return [command1, command2]


@pytest.fixture
def domain_command_results():
    command_result_1 = models.CommandResult(
        status='status11', message='message11', data={'key11', 'value11'})

    command_result_2 = models.CommandResult(
        status='status21', message='message21', data={'key21', 'value21'})

    return [command_result_1, command_result_2]


def test_command_execute_use_case(domain_command_requests,
                                  domain_command_results, mocker):
    endpoint = mocker.Mock()
    endpoint.exec.side_effect = domain_command_results

    command_execute_use_case = uc.CommandExecuteUseCase(endpoint)

    for command, result in zip(domain_command_requests,
                               domain_command_results):

        request_object = req.CommandExecuteRequestObject.from_dict(command)
        response_object = command_execute_use_case.execute(request_object)

        assert response_object.value == result
