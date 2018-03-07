#! /usr/bin/env python

"""
    File name: discipline.py
    Author: Dimitar Petrov
    Date created: 2018/03/02
    Python Version: 3.6
    Description: Improves presence/mindfulness and self-control
"""

import os
import time
import subprocess
import crypt
from decouple import config

class PassChanger():
    """Implementing password change for linux"""
    def __init__(self, pw_length=12):
        self.pw_length = pw_length
        self.hashdict = {config('LOGIN'): config('PASSHASH')}

    @staticmethod
    def change_pass(user, pass_hash):
        """Change loging password with pass_hash"""
        ret_val = subprocess.call(('sudo', 'usermod', '-p', pass_hash, user))
        if ret_val != 0:
            print('Error changing password for {}'.format(user))

    def generate_passphrase(self):
        """Generate random passphrase using pwgen"""
        passphrase = subprocess.check_output(['pwgen', str(self.pw_length), '1'])
        passphrase = passphrase.decode('utf-8').strip()
        return passphrase

    def set_random_pass(self, user):
        """Set random password to user"""
        salt = os.urandom(16)
        password = self.generate_passphrase()
        pass_hash = crypt.crypt(password, '$1${}$'.format(salt))
        self.change_pass(user, pass_hash)

    def restore_pass(self, user):
        """Restore old password of user user"""
        self.change_pass(user, self.hashdict[user])

class ScreenLocker():
    """Lock the screen and change loging password"""
    def __init__(self, user):
        self.pass_changer = PassChanger()
        self.user = user

    @staticmethod
    def lock():
        """Execute i3lock with specific parameters"""
        subprocess.call(('i3lock', '-c', '000000', '-f'))

    @staticmethod
    def unlock():
        """Unlock the screen"""
        subprocess.call(('pkill', 'i3lock'))

    def secure_lock(self, wait=30):
        """Change user password and lock screen.
        After wait time restore the original password"""
        self.pass_changer.set_random_pass(self.user)
        self.lock()
        time.sleep(int(wait))
        self.pass_changer.restore_pass(self.user)
