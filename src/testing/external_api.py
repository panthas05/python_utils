from collections.abc import Callable
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import random
from socketserver import BaseRequestHandler
from typing import Any, ClassVar
from threading import Thread
from urllib.parse import parse_qsl, ParseResult, urlparse
from unittest import TestCase


class WebRequestHandler(BaseHTTPRequestHandler):
    """
    Class to be subclassed for creating stubs representing external APIs.
    """

    @cached_property
    def url(self) -> ParseResult:
        return urlparse(self.path)

    @cached_property
    def query_data(self) -> dict:
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self) -> bytes:
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self) -> dict:
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def json(self) -> dict:
        request_json: dict = json.loads(self.post_data.decode("utf-8"))
        return request_json

    @cached_property
    def cookies(self) -> SimpleCookie:
        return SimpleCookie(self.headers.get("Cookie"))

    def return_empty_error_response(self) -> None:
        self.send_response(500)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"")


RequestHandler = Callable[[Any, Any, HTTPServer], BaseRequestHandler]


class ExternalApiTestCase(TestCase):
    """
    Launches a simple webserver for the duration of the TestSuite subclassing
    this TestCase, whose behaviour is defined by the RequestHandlerClass
    attribute on the subclass. One can then patch out urls in the code to make
    their requests to this webserver instead of the actual API endpoints, and
    get the webserver to return the appropriate/expected data from the server.
    """

    test_server_host: str = "127.0.0.1"
    test_server_port: int = random.randrange(9000, 11000)

    @property
    def test_server_base_url(self) -> str:
        return f"http://{self.test_server_host}:{self.test_server_port}"

    RequestHandlerClass: RequestHandler

    def __init_subclass__(
        cls,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        request_handler_class = getattr(cls, "RequestHandlerClass", None)
        if request_handler_class is None or not issubclass(
            request_handler_class,
            WebRequestHandler,
        ):
            raise TypeError(
                f"{cls.__name__} needs a RequestHandlerClass attribute, which "
                "is (typically) a subclass of WebRequestHandler."
            )
        super().__init_subclass__(*args, **kwargs)

    _server: HTTPServer

    @classmethod
    def launch_server(cls) -> None:
        try:
            cls._server = HTTPServer(
                (cls.test_server_host, cls.test_server_port),
                cls.RequestHandlerClass,
            )
            Thread(
                target=cls._server.serve_forever,
                name=f"{cls.__name__} test server",
                daemon=True,
                kwargs={"poll_interval": 0.01},
            ).start()
        except Exception:
            logging.exception(
                "Exception occurred whilst launching test server in " f"{cls.__name__}"
            )
            cls.shutdown_server()

    @classmethod
    def shutdown_server(cls) -> None:
        if hasattr(cls, "_server"):
            cls._server.shutdown()
            cls._server.server_close()
            del cls._server

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.launch_server()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.shutdown_server()
