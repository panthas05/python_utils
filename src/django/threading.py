from django.conf import settings

from .database import disconnect_db_afterwards
from src.types import GenericFunction, ThreadedFunction

from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
import functools
from typing import Any, Protocol

DEFAULT_MAXIMUM_WORKER_THREADS = 5

_global_executor = ThreadPoolExecutor(
    max_workers=getattr(settings, "MAXIMUM_WORKER_THREADS", None)
    or DEFAULT_MAXIMUM_WORKER_THREADS
)


def run_in_thread(
    function: GenericFunction,
) -> ThreadedFunction:

    @functools.wraps(function)
    def inner_function(
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]:
        # we need the called function to close the database connection in the
        # thread, so create another function which simply calls the function
        # whilst being decorated by disconnect_db_afterwards
        @disconnect_db_afterwards
        def wrapped_function(
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            return function(*args, **kwargs)

        return _global_executor.submit(
            wrapped_function,
            *args,
            **kwargs,
        )

    return inner_function
