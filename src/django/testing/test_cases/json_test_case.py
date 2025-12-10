from django.http import JsonResponse
from django.test import TestCase, RequestFactory

from src import types

import json
from typing import Any


class JsonTestCase(TestCase):
    request_factory = RequestFactory()

    def extract_response_json(
        self,
        response: JsonResponse,
    ) -> types.JSON:
        """
        Extracts and parses the payload of a JsonResponse, returning a dict
        holding the object's keys and values.
        """
        response_json: types.JSON = json.loads(response.content.decode())
        return response_json
