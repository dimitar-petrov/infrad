#! /usr/bin/env python

"""
    File name: models.py
    Author: Dimitar Petrov
    Date created: 2018/03/30
    Python Version: 3.6
    Description: Data models used in infrad
"""
from infrad.shared.domain_model import DomainModel


class Command:
    """Model for storing commands"""
    def __init__(self, module, action, args, kwargs):
        self.module = module
        self.action = action
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_dict(cls, adict):
        """Initializer from a dictionary"""
        command = cls(
            module=adict['module'],
            action=adict['action'],
            args=adict['args'],
            kwargs=adict['kwargs'])

        return command


class CommandResult:
    """Model for storing output of commands"""
    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data

    @classmethod
    def from_dict(cls, adict):
        """Initializer from a dictionary"""
        result = cls(
            status=adict['status'],
            message=adict['message'],
            data=adict['data'])

        return result


DomainModel.register(Command)
DomainModel.register(CommandResult)
