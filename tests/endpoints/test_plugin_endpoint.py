import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from infrad.endpoints import plugin_endpoint as pe
import infrad.domain.models as m
from infrad.shared.consts import JobState


def test_plugin_endpoint_init():
    endpoint = pe.PluginEndpoint()

    assert isinstance(endpoint.executor, ThreadPoolExecutor)


def test_plugin_endpoint_sync_command_success(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.return_value = 'job completed successfully'
    pe.Plugin.plugins = [mock]


    result = endpoint.exec('comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Sync Execution Finished'
    assert result.data == "job completed successfully"
    assert result.status == JobState.COMPLETED


def test_plugin_endpoint_sync_command_fail(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.return_value = 'job completed successfully'
    pe.Plugin.plugins = [mock]


    result = endpoint.exec('missing_comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Command not found'
    assert result.data == None
    assert result.status == JobState.FAILED


# @pytest.mark.skip
def test_plugin_endpoint_async_command_success(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.side_effect = lambda *args, **kwargs: time.sleep(0.01)
    pe.Plugin.plugins = [mock]

    result = endpoint.exec('comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Async Execution In Progress'
    assert result.status == JobState.RUNNING
    assert result.data == None


def test_plugin_endpoint_async_command_fail(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.side_effect = ['out']
    pe.Plugin.plugins = [mock]


    result = endpoint.exec('missing_comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Command not found'
    assert result.status == JobState.FAILED
    assert result.data == None
