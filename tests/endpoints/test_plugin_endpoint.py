import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from infrad.endpoints import plugin_endpoint as pe
from infrad.plugin import Plugin
import infrad.domain.models as m
from infrad.shared.consts import JOB_STATE


def test_plugin_endpoint_init():
    endpoint = pe.PluginEndpoint()

    assert isinstance(endpoint.executor, ThreadPoolExecutor)


def test_plugin_endpoint_sync_command_success(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.return_value = 'job completed successfully'
    Plugin.plugins = [mock]


    result = endpoint.exec('comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Sync Execution Finished'
    assert result.data == "job completed successfully"
    assert result.status == JOB_STATE.COMPLETED

def test_plugin_endpoint_sync_command_fail(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.return_value = 'job completed successfully'
    Plugin.plugins = [mock]


    result = endpoint.exec('missing_comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Command not found'
    assert result.data == None
    assert result.status == JOB_STATE.FAILED


# @pytest.mark.skip
def test_plugin_endpoint_async_command_success(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.side_effect = lambda *args, **kwargs: time.sleep(0.01)
    Plugin.plugins = [mock]

    result = endpoint.exec('comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Async Execution In Progress'
    assert result.status == JOB_STATE.RUNNING
    assert result.data == None

def test_plugin_endpoint_async_command_fail(mocker):
    endpoint = pe.PluginEndpoint()

    mock = mocker.Mock()
    mock.init_command = 'comm'
    mock.do_work.side_effect = ['out']
    Plugin.plugins = [mock]


    result = endpoint.exec('missing_comm', ['arg1', 'arg2'], {'kwarg1': 'value1'})

    assert isinstance(result, m.CommandResult)
    assert result.message == 'Command not found'
    assert result.status == JOB_STATE.FAILED
    assert result.data == None
