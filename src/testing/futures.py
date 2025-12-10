from asyncio import Future
from typing import Any
from unittest import mock


class MockFutureFactory:
    def with_exception(self, exception: BaseException) -> mock.MagicMock:
        mock_future = mock.MagicMock(spec=Future)
        mock_future.exception = lambda: exception
        mock_future.result = lambda: None
        return mock_future

    def with_result(self, result: Any) -> mock.MagicMock:
        mock_future = mock.MagicMock(spec=Future)
        mock_future.result = lambda: result
        mock_future.exception = lambda: None
        return mock_future
