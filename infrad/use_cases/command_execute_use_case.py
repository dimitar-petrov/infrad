#! /usr/bin/env python
"""
    File name: execute_command_use_case.py
    Author: Dimitar Petrov
    Date created: 2018/04/01
    Python Version: 3.6
    Description: Use case that executes command
"""
from infrad.shared import use_case as uc
from infrad.shared import response_object as res


class CommandExecuteUseCase(uc.UseCase):
    """Execute the command on registered endpoint.

    Attributes:
        endpoint (str): Endpoint plugin implementing execution.

    """

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def process_request(self, request_object):
        """Forward command to endpoint and return result.

        Args:
        request_object (CommandExecuteRequestObject): Request Object.

        Returns:
        ResponseObject: Encapsulated return value from the endpoint.
        """
        # TODO: fix this pass of request object
        # Backend layer should not be aware of request_object

        command_result = self.endpoint.exec(
            module=request_object.module,
            action=request_object.action,
            args=request_object.args,
            kwargs=request_object.kwargs,
            sync=request_object.sync)

        return res.ResponseSuccess(command_result)
