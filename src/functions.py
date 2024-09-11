from collections.abc import Awaitable, Callable
from typing import TypeVar


T = TypeVar("T")  # i.e. a generic from Dart

PostException = Callable[[], None] | None


# TODO: can we rewrite the following as decorators?
def retry(
    function: Callable[[], T],
    post_exception: PostException = None,
    retry_count: int = 3,
) -> T:
    """
    Retries a function a certain number of times, catching generic exceptions on
    each invocation, but re-raising them when the threshold has been hit. The
    post_exception function will be called before the exception is reraised, if
    the call fails the maximum number of times that it can.
    """
    threshold = retry_count - 1
    for x in range(retry_count):
        try:
            ret = function()
            break
        except Exception:
            # perhaps we should change this s.t. post_exception takes the
            # exception as an argument, then it can e.g. rethrow, do some
            # logging, etc
            if post_exception:
                post_exception()
            if x == threshold:
                raise
    return ret


APostException = Callable[[], Awaitable[None]] | None


async def aretry(
    afunction: Callable[[], Awaitable[T]],
    post_exception: APostException = None,
    retry_count: int = 3,
) -> T:
    """
    Asynchronous version of retry.
    """
    threshold = retry_count - 1
    for x in range(retry_count):
        try:
            ret = await afunction()
            break
        except Exception as e:
            if post_exception:
                await post_exception()
            if x == threshold:
                raise e
    return ret
