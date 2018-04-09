from infrad.domain import models as m


def test_command_model_init():
    command = m.Command(
        'module',
        'action',
        args=['arg1', 'arg2'],
        kwargs={
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        })

    assert command.module == 'module'
    assert command.action == 'action'
    assert command.args == ['arg1', 'arg2']
    assert command.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}


def test_command_model_from_dict():
    command = m.Command.from_dict({
        'module': 'module',
        'action': 'action',
        'args': ['arg1', 'arg2'],
        'kwargs': {
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        }})

    assert command.module == 'module'
    assert command.action == 'action'
    assert command.args == ['arg1', 'arg2']
    assert command.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}
