from infrad.domain import models as m


def test_command_model_init():
    command = m.Command(
        'command',
        args=['arg1', 'arg2'],
        kwargs={
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        },
        sync=True)

    assert command.comm == 'command'
    assert command.args == ['arg1', 'arg2']
    assert command.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}
    assert command.sync is True


def test_command_model_from_dict():
    command = m.Command.from_dict({
        'comm': 'command',
        'args': ['arg1', 'arg2'],
        'kwargs': {
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        },
        'sync': True
    })

    assert command.comm == 'command'
    assert command.args == ['arg1', 'arg2']
    assert command.kwargs == {'kwarg1': 'value1', 'kwarg2': 'value2'}
    assert command.sync is True
