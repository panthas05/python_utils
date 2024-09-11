from django.conf import settings
from django.db import close_old_connections, connection

from src.types import GenericFunction

from functools import wraps
import logging
import time
from typing import Any


def disconnect_db_afterwards(function: GenericFunction) -> GenericFunction:
    @wraps(function)
    def inner_function(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        finally:
            close_old_connections()

    return inner_function


def mutex(
    name: str | None = None,
    timeout: int = 5,
) -> Any:
    """
    For use with postgres only. Requires the settings MUTEX_NAMESPACE to be
    defined to function.
    """

    def wrap(function: GenericFunction) -> GenericFunction:
        @wraps(function)
        def inner_function(*args: Any, **kwargs: Any) -> Any:
            nonlocal name
            name = name or (
                f"{function.__module__.replace('.', '_')}_{function.__name__}"
            )
            mutex_name = f"{settings.MUTEX_NAMESPACE}_mutex_{name}"

            cursor = connection.cursor()
            for i in range(timeout):
                cursor.execute("SELECT pg_try_advisory_lock(%s)", (hash(mutex_name),))
                ((got_mutex,),) = cursor.fetchall()
                if got_mutex:
                    break
                time.sleep(1)

            ret = None
            if got_mutex:
                try:
                    ret = function(*args, **kwargs)
                finally:
                    cursor.execute("SELECT pg_advisory_unlock(%s)", (hash(mutex_name),))
            else:
                logging.info(
                    f"Not running {function.__name__}, {mutex_name} mutex not available"
                )
            return ret

        return inner_function

    return wrap
