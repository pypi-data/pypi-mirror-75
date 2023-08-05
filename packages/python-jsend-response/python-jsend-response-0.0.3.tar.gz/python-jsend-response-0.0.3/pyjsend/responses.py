import json


class BaseResponse:
    message = None
    data = None
    status = None
    http_code = None

    def to_json(self):
        response = {}

        if self.data:
            response['data'] = self.data
        else:
            response['message'] = self.message

        response['code'] = self.http_code
        response['type'] = self.__class__.__name__

        return json.dumps(response)


class SuccessResponse(BaseResponse):

    status = 'success'
    http_code = 200

    def __init__(self, data={}):
        self.data = data


class CreatedSuccessfully(SuccessResponse):
    http_code = 201


class FailureResponse(BaseResponse):
    status = 'failure'
    http_code = 400

    def __init__(self, message=None):
        self.message = message


class ErrorResponse(BaseResponse):
    status = 'error'
    http_code = 500

    def __init__(self, message=None):
        self.message = message


class BadResponse(FailureResponse):
    def __init__(self, message='Bad Request'):
        self.message = message


class Unauthorized(FailureResponse):
    http_code = 401

    def __init__(self, message='Unauthorized'):
        self.message = message


class Forbidden(FailureResponse):
    http_code = 403

    def __init__(self, message="Forbidden"):
        self.message = message


class NotFound(FailureResponse):
    http_code = 404

    def __init__(self, message="Not found"):
        self.message = message


class ValidationError(BadResponse):

    def __init__(self, message="The fields specified are invalid."):
        self.message = message


class WrongData(BadResponse):

    def __init__(self, message="The fields specified are invalid."):
        self.message = message


class ServerError(ErrorResponse):

    def __init__(self, message="Server error."):
        self.message = message
