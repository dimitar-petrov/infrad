import collections
from infrad.shared import request_object as req


class CommandExecuteRequestObject(req.ValidRequestObject):
    """Request object encapsulating incoming API calls.

    Attributes:
        attr1 (str): Description of YY.
        attr2 (:obj:YY, optional): Description of Y.

    """
    def __init__(self, module, action, args, kwargs, sync=False):
        self.module = module
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.sync = sync

    @classmethod
    def from_dict(cls, adict):
        """Initializer from a dictionary"""

        invalid_req = req.InvalidRequestObject()

        if 'module' not in adict:
            invalid_req.add_error('module', 'Is mandatory')
        elif not isinstance(adict['module'], str):
            invalid_req.add_error('module', 'Is not str')

        if 'action' not in adict:
            invalid_req.add_error('action', 'Is mandatory')
        elif not isinstance(adict['action'], str):
            invalid_req.add_error('action', 'Is not str')

        if 'args' in adict and not isinstance(adict['args'], list):
            invalid_req.add_error('args', 'Is not list')

        if 'kwargs' in adict and not isinstance(adict['kwargs'],
                                                collections.Mapping):
            invalid_req.add_error('kwargs', 'Is not mapping')

        if invalid_req.has_errors():
            return invalid_req

        return CommandExecuteRequestObject(
            module=adict['module'],
            action=adict['action'],
            args=adict.get('args', list()),
            kwargs=adict.get('kwargs', dict()),
            sync=adict.get('sync', False))
