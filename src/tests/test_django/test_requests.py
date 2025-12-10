from unittest import TestCase

from django.test import RequestFactory

from . import django_test_case
from src.django import requests


class GetRequestIpAddressTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    request_factory = RequestFactory()
    public_ip = "9.188.1.3"
    other_public_ip = "9.188.1.4"

    def test_extracts_remote_address(self) -> None:
        request = self.request_factory.get("/")
        request.META["REMOTE_ADDR"] = self.public_ip
        self.assertEqual(requests.get_request_ip_address(request), self.public_ip)

    def test_forwarded_for_overrides_remote_address(self) -> None:
        request = self.request_factory.get("/")
        request.META["REMOTE_ADDR"] = self.public_ip
        request.META["HTTP_X_FORWARDED_FOR"] = self.other_public_ip
        self.assertEqual(requests.get_request_ip_address(request), self.other_public_ip)

    def test_remote_address_skips_private_ips(self) -> None:
        request = self.request_factory.get("/")
        request.META["REMOTE_ADDR"] = "10.188.1.3"
        self.assertEqual(requests.get_request_ip_address(request), "")

    def test_forwarded_for_skips_private_ips(self) -> None:
        request = self.request_factory.get("/")
        request.META["HTTP_X_FORWARDED_FOR"] = ",".join(
            (
                "10.188.1.3\n",  # private, should be skipped
                " 172.123.1.3",  # private, should be skipped
                "192.188.1.3    ",  # private, should be skipped
                "",  # just to mess with it ;)
                "\r",  # just to mess with it ;)
                self.public_ip,  # public, should override remote addr
            )
        )
        self.assertEqual(requests.get_request_ip_address(request), self.public_ip)
