
from pyjsend.responses import SuccessResponse, BadResponse


def test_json_schema_invalid_input():

    response = BadResponse()

    assert response.http_code == 400


def test_json_schema_success_code():
    email = 'some@email.com'

    response = SuccessResponse(data={'email': email})

    assert response.http_code == 200


def test_json_schema_to_json_method():
    email = 'some@email.com'

    response = SuccessResponse({'email': email})

    assert response.to_json()
