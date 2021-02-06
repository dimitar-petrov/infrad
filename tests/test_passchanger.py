import os
import pytest
import subprocess
import crypt
import decouple
from decouple import UndefinedValueError
from infrad.endpoints import discipline

TEST_USER = 'test_user'
TEST_PASSHASH = 'test_passhash'
PW_LENGTH = 12


@pytest.fixture
def passchanger():
    passchanger = discipline.PassChanger(
        pw_length=PW_LENGTH, username=TEST_USER, passhash=TEST_PASSHASH)
    return passchanger


@pytest.mark.skip
def test_missing_config_exception(mocker):
    mock = mocker.patch('decouple.config.SUPPORTED')
    mock.return_value = dict()
    decouple.config.config = None
    with pytest.raises(UndefinedValueError):
        discipline.PassChanger()


def test_generate_passphrase(mocker, passchanger):
    mocker.patch('subprocess.check_output')
    passchanger.generate_passphrase()

    subprocess.check_output.assert_called_once_with(
        ['pwgen', str(PW_LENGTH), '1'])


def test_change_pass(mocker, passchanger):
    mocker.patch('subprocess.call')
    passchanger.change_pass(TEST_USER, TEST_PASSHASH)

    subprocess.call.assert_called_once_with(
        ('sudo', 'usermod', '-p', TEST_PASSHASH, TEST_USER))


def test_set_random_pass(mocker, passchanger):
    mocker.patch.object(passchanger, 'change_pass')
    mocker.patch.object(passchanger, 'generate_passphrase')
    mocker.patch('crypt.crypt')

    passchanger.generate_passphrase.return_value = 'random_pass'

    passchanger.set_random_pass(TEST_USER)

    passchanger.change_pass.assert_called_once()
    crypt.crypt.assert_called_once()


def test_restore_pass(mocker, passchanger):
    mocker.patch.object(passchanger, 'change_pass')
    passchanger.restore_pass(TEST_USER)

    passchanger.change_pass.assert_called_once_with(TEST_USER, TEST_PASSHASH)
