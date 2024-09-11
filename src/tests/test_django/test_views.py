from django.http import HttpResponseBadRequest, HttpResponse
from django.test import RequestFactory

from . import django_test_case
from unittest import TestCase

from src.django import views


class AcceptOnlyTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    request_factory = RequestFactory()

    def test_raises_if_no_methods_provided(self):
        with self.assertRaisesRegex(
            ValueError,
            "No methods provided to accept_only decorator.",
        ) as context_manager:

            @views.accept_only([])
            def dummy_view(request):
                return HttpResponse("OK")

    def test_blocks_forbidden_methods(self):
        @views.accept_only(["POST"])
        def dummy_view(request):
            return HttpResponse("OK")

        response = dummy_view(self.request_factory.get("/"))
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertEqual(response.content.decode(), "Only accepts POST requests.")

    def test_permits_accepted_methods(self):
        @views.accept_only(["GET"])
        def dummy_view(request):
            return HttpResponse("OK")

        response = dummy_view(self.request_factory.get("/"))
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content.decode(), "OK")
