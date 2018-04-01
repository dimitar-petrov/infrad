import collections
from infrad.shared import request_object as req


class CommandExecuteRequestObject(req.ValidRequestObject):
    """Request object encapsulating incoming API calls.

    Attributes:
        attr1 (str): Description of YY.
        attr2 (:obj:YY, optional): Description of Y.

    """
    def __init__(self, comm, args, kwargs, sync=False):
        self.comm = comm
        self.args = args
        self.kwargs = kwargs
        self.sync = sync

    @classmethod
    def from_dict(cls, adict):
        """Initializer from a dictionary"""

        invalid_req = req.InvalidRequestObject()

        if 'comm' not in adict:
            invalid_req.add_error('comm', 'Is mandatory')
        elif not isinstance(adict['comm'], str):
            invalid_req.add_error('comm', 'Is not str')

        if 'args' in adict and not isinstance(adict['args'], list):
            invalid_req.add_error('args', 'Is not list')

        if 'kwargs' in adict and not isinstance(adict['kwargs'],
                                                collections.Mapping):
            invalid_req.add_error('kwargs', 'Is not mapping')

        if invalid_req.has_errors():
            return invalid_req

        return CommandExecuteRequestObject(
            comm=adict['comm'],
            args=adict.get('args', list()),
            kwargs=adict.get('kwargs', dict()),
            sync=adict.get('sync', False))
