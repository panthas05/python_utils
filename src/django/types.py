from django.http import HttpRequest, HttpResponse

from collections.abc import Callable
from typing import Any, Protocol


class View(Protocol):

    def __call__(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse: ...
