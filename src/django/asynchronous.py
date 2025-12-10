from django.http import HttpRequest

from src.django import logging

from typing import TypeVar

T = TypeVar("T")

# TODO: move this to a function iterables perhaps


def extract_results_with_logging(
    results_and_exceptions: list[T | BaseException], request: HttpRequest | None = None
) -> list[T]:
    raised_exceptions = [
        e for e in results_and_exceptions if isinstance(e, BaseException)
    ]
    # if (
    #     len(raised_exceptions) == len(results_and_exceptions)
    #     and len(raised_exceptions) > 0
    # ):
    #     promoted_exceptions = [
    #         exceptions.promote_base_exception(e) for e in raised_exceptions
    #     ]
    #     raise ExceptionGroup("All futures raised exceptions.", promoted_exceptions)
    # else:
    for exception in raised_exceptions:
        logging.send_error_email(exception, request=request)
    return [r for r in results_and_exceptions if not isinstance(r, BaseException)]
