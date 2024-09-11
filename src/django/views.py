from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

from .types import View

from collections.abc import Callable
import functools
from typing import Any


def accept_only(
    methods: list[str],
) -> Callable[[View], View]:
    methods = sorted([m.upper() for m in methods])
    if len(methods) == 0:
        raise ValueError("No methods provided to accept_only decorator.")

    methods_summary = (
        f"{', '.join(methods[:-1])}, and {methods[-1]}"
        if len(methods) > 1
        else methods[0]
    )
    methods_summary = f"Only accepts {methods_summary} requests."

    def decorator(wrapped_view: View) -> View:
        @functools.wraps(wrapped_view)
        def view(
            request: HttpRequest,
            *args: Any,
            **kwargs: Any,
        ) -> HttpResponse:
            if request.method not in methods:
                return HttpResponseBadRequest(methods_summary)
            return wrapped_view(request, *args, **kwargs)

        return view

    return decorator
