from infrad.shared import request_object as req


def test_invalid_request_object_accepts_errors():
    request = req.InvalidRequestObject()
    request.add_error(parameter='param1', message='wrong value')
    request.add_error(parameter='param2', message='wrong type')

    assert request.has_errors() is True
    assert len(request.errors) == 2


def test_valid_request_object_is_true():
    request = req.ValidRequestObject()

    assert bool(request) is True
