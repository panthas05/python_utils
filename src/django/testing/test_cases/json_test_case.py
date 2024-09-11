from django.http import JsonResponse
from django.test import TestCase, RequestFactory

import json


class JsonTestCase(TestCase):
    request_factory = RequestFactory()

    def extract_response_json(self, response: JsonResponse) -> dict:
        """
        Extracts and parses the payload of a JsonResponse, returning a dict
        holding the object's keys and values.
        """
        response_json: dict = json.loads(response.content.decode())
        return response_json
