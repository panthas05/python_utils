from django.conf import settings
from django.http import HttpRequest

from src.types import GenericFunction

from functools import wraps
import logging
from typing import Any


def send_error_email(
    exception: BaseException,
    request: HttpRequest | None = None,
) -> None:
    logger = logging.getLogger("django.request")
    extra: dict[str, int | HttpRequest] = {"status_code": 500}
    if request:
        extra["request"] = request
    if getattr(settings, "LOG_ERRORS", None) is False:
        return
    logger.error(
        repr(exception),
        exc_info=exception,
        stack_info=True,
        extra=extra,
    )


def log_errors(
    function: GenericFunction,
    request: HttpRequest | None = None,
) -> GenericFunction:
    @wraps(function)
    def inner_function(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except Exception as e:
            send_error_email(e)
            raise

    return inner_function
