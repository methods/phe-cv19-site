import json
from requests.models import Response
from http import HTTPStatus


class DummyMocks:

    @classmethod
    def get_successful_load_content(cls):
        return {
            "key": "Some data loaded"
        }

    @classmethod
    def get_successful_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_load_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response
