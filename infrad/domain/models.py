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
    def __init__(self, comm, args, kwargs, sync=False):
        self.comm = comm
        self.args = args
        self.kwargs = kwargs
        self.sync = sync

    @classmethod
    def from_dict(cls, adict):
        """Initializer from a dictionary"""
        command = cls(
            comm=adict['comm'],
            args=adict['args'],
            kwargs=adict['kwargs'],
            sync=adict['sync'])

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
