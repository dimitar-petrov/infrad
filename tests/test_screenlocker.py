import pytest
import subprocess
from infrad import discipline

TEST_USER = 'test_user'

@pytest.fixture
def screenlocker():
    screenlocker = discipline.ScreenLocker(user=TEST_USER)
    return screenlocker

def test_lock(mocker, screenlocker):
    with mocker.patch('subprocess.call') as mock:
        screenlocker.lock()

    subprocess.call.assert_called_once_with(('i3lock', '-c', '000000', '-f'))


def test_secure_lock(mocker, screenlocker):
    mocker.patch.object(screenlocker.pass_changer, 'set_random_pass')
    mocker.patch.object(screenlocker.pass_changer, 'restore_pass')
    mocker.patch.object(screenlocker, 'lock')
    screenlocker.secure_lock(wait=0)

    screenlocker.pass_changer.set_random_pass.assert_called_with(TEST_USER)
    screenlocker.lock.assert_called_once()
    screenlocker.pass_changer.restore_pass.assert_called_with(TEST_USER)

def test_unlock(mocker, screenlocker):
    with mocker.patch('subprocess.call') as mock:
        screenlocker.unlock()

    subprocess.call.assert_called_once_with(('pkill', 'i3lock'))
