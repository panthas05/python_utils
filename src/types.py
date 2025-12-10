from collections.abc import Callable
from concurrent.futures import Future
from typing import Any, Protocol


class GenericFunction(Protocol):

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...

    __name__: str


class ThreadedFunction(Protocol):

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]: ...
