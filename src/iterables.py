from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")
S = TypeVar("S")


def first_where(
    iterable: Iterable[T],
    condition: Callable[[T], bool],
    fallback: S | None,
) -> T | S | None:
    """
    Returns the first element of an iterable which satisfies the required
    condition, or fallback if none do.
    """
    if not callable(condition):
        raise TypeError(
            '"condition" passed to first_where should be a callable '
            "function which returns a boolean."
        )
    return next((i for i in iterable if condition(i)), fallback)


def chunks(
    sized_iterable: Sequence[T],
    n: int,
) -> Generator[Sequence[T], None, None]:
    """
    Yield successive n-sized chunks from sized_iterable.
    """
    for i in range(0, len(sized_iterable), n):
        yield sized_iterable[i : i + n]
