from unittest import IsolatedAsyncioTestCase, TestCase, mock

from src import functions


class TestException(Exception):
    pass


def throw_exception() -> None:
    raise TestException


function_that_throws = mock.Mock(side_effect=throw_exception)


class RetryTests(TestCase):
    def tearDown(self) -> None:
        super().tearDown()
        function_that_throws.reset_mock()

    def test_reraises(self) -> None:
        with self.assertRaises(TestException):
            functions.retry(function_that_throws)
        # the default retry_count is 3, this can be changed
        self.assertEqual(function_that_throws.call_count, 3)

    def test_respects_retry_count(self) -> None:
        with self.assertRaises(TestException):
            functions.retry(function_that_throws, retry_count=4)
        self.assertEqual(function_that_throws.call_count, 4)

    def test_calls_post_exception(self) -> None:
        post_exception = mock.Mock()
        with self.assertRaises(TestException):
            functions.retry(function_that_throws, post_exception=post_exception)
        # the default retry_count is 3, this can be changed
        self.assertEqual(post_exception.call_count, 3)


afunction_which_throws = mock.AsyncMock(side_effect=throw_exception)


class ARetryTests(IsolatedAsyncioTestCase):
    def tearDown(self) -> None:
        super().tearDown()
        afunction_which_throws.reset_mock()

    async def test_reraises(self) -> None:
        with self.assertRaises(TestException):
            await functions.aretry(afunction_which_throws)
        # the default retry_count is 3, this can be changed
        self.assertEqual(afunction_which_throws.call_count, 3)

    async def test_respects_retry_count(self) -> None:
        with self.assertRaises(TestException):
            await functions.aretry(afunction_which_throws, retry_count=4)
        self.assertEqual(afunction_which_throws.call_count, 4)

    async def test_calls_post_exception(self) -> None:
        post_exception = mock.AsyncMock()
        with self.assertRaises(TestException):
            await functions.aretry(
                afunction_which_throws, post_exception=post_exception
            )
        # the default retry_count is 3, this can be changed
        self.assertEqual(post_exception.call_count, 3)
