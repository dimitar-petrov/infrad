#! /usr/bin/env python

"""
    File name: use_case.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Action execution use case
"""
from infrad.shared import response_object as res


class UseCase:
    """Base class for execution use cases in infrad."""
    def execute(self, request_object):
        """Example function with types documented in the docstring.

        Args:
        request_object (CommandExecuteRequestObject):
        Encapsulated request information.

        Returns:
        ResponseFailure or ResponseSuccess object
        """
        if not request_object:
            return res.ResponseFailure.build_from_invalid_request_object(
                request_object)
        try:
            return self.process_request(request_object)
        except Exception as exc:  # pylint: disable-msg=W0703
            "{}: {}".format(exc.__class__.__name__, "{}".format(exc))

    def process_request(self, request_object):
        """Abstract method that has to be implemented
        by inheriting use cases."""
        raise NotImplementedError(
            'process_request() not implemented by UseCase class')
