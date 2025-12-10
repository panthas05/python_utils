from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.http import HttpRequest
from django.test import TestCase


class SessionTestCase(TestCase):
    session_middleware = SessionMiddleware(lambda x: x)
    message_middleware = MessageMiddleware(lambda x: x)

    def add_session(self, request: HttpRequest) -> HttpRequest:
        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        return request
