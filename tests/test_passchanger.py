import os
import pytest
import subprocess
import crypt
from context import discipline
from decouple import config, UndefinedValueError

TEST_USER = 'test_user'
TEST_PASSHASH = 'test_passhash'

@pytest.fixture
def passchanger():
    os.environ["LOGIN"] = TEST_USER
    os.environ["PASSHASH"] = TEST_PASSHASH
    passchanger = discipline.PassChanger()
    return passchanger

def test_missing_config_exception(mocker):
    with mocker.patch('decouple.config.SUPPORTED') as mock:
        mock.return_value = dict()
        with pytest.raises(UndefinedValueError):
            passchanger = discipline.PassChanger()

def test_generate_passphrase(passchanger):
    assert isinstance(passchanger.generate_passphrase(), str)
    assert len(passchanger.generate_passphrase()) == passchanger.pw_length

def test_change_pass(mocker, passchanger):
    with mocker.patch('subprocess.call'):
        passchanger.change_pass(TEST_USER, TEST_PASSHASH)

    subprocess.call.assert_called_once_with(('sudo', 'usermod', '-p', TEST_PASSHASH, TEST_USER))


def test_set_random_pass(mocker, passchanger):
    mocker.patch.object(passchanger, 'change_pass')
    mocker.patch('crypt.crypt')
    passchanger.set_random_pass(TEST_USER)

    passchanger.change_pass.assert_called_once()
    crypt.crypt.assert_called_once()

def test_restore_pass(mocker, passchanger):
    with mocker.patch.object(passchanger, 'change_pass'):
        passchanger.restore_pass(TEST_USER)

    passchanger.change_pass.assert_called_once_with(TEST_USER, TEST_PASSHASH)


