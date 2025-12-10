from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import RequestFactory, TestCase

from typing import Any, ClassVar


class StaffMemberRequiredTestCase(TestCase):
    request_factory = RequestFactory()
    staff_user: ClassVar[Any]
    staff_user_username = "staffuser"
    staff_user_password = "password"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.staff_user = get_user_model().objects.create_user(
            cls.staff_user_username,
            password=cls.staff_user_password,
            email="staff.user@thegoodbook.com",
            is_staff=True,
        )

    def get_staff_member_request(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> HttpRequest:
        request_builder = {
            "GET": self.request_factory.get,
            "POST": self.request_factory.post,
            "PATCH": self.request_factory.patch,
            "PUT": self.request_factory.put,
            "DELETE": self.request_factory.delete,
        }[method.upper()]
        request: HttpRequest = request_builder(*args, **kwargs)  # type: ignore
        request.user = self.staff_user
        return request
