import os
import pytest
import subprocess
import crypt
import decouple
from decouple import UndefinedValueError
from infrad import discipline

TEST_USER = 'test_user'
TEST_PASSHASH = 'test_passhash'
PW_LENGTH = 12

@pytest.fixture
def passchanger():
    os.environ["LOGIN"] = TEST_USER
    os.environ["PASSHASH"] = TEST_PASSHASH
    passchanger = discipline.PassChanger(pw_length=PW_LENGTH)
    return passchanger

def test_missing_config_exception(mocker):
    with mocker.patch('decouple.config.SUPPORTED') as mock:
        mock.return_value = dict()
        decouple.config.config = None
        with pytest.raises(UndefinedValueError):
            passchanger = discipline.PassChanger()

def test_generate_passphrase(mocker, passchanger):
    with mocker.patch('subprocess.check_output'):
        passchanger.generate_passphrase()

    subprocess.check_output.assert_called_once_with(['pwgen', str(PW_LENGTH), '1'])

def test_change_pass(mocker, passchanger):
    with mocker.patch('subprocess.call'):
        passchanger.change_pass(TEST_USER, TEST_PASSHASH)

    subprocess.call.assert_called_once_with(('sudo', 'usermod', '-p', TEST_PASSHASH, TEST_USER))


def test_set_random_pass(mocker, passchanger):
    mocker.patch.object(passchanger, 'change_pass')
    mocker.patch.object(passchanger, 'generate_passphrase')
    mocker.patch('crypt.crypt')

    passchanger.generate_passphrase.return_value = 'random_pass'

    passchanger.set_random_pass(TEST_USER)

    passchanger.change_pass.assert_called_once()
    crypt.crypt.assert_called_once()

def test_restore_pass(mocker, passchanger):
    with mocker.patch.object(passchanger, 'change_pass'):
        passchanger.restore_pass(TEST_USER)

    passchanger.change_pass.assert_called_once_with(TEST_USER, TEST_PASSHASH)


