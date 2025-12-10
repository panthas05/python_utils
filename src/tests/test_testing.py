from unittest import TestCase

from src.testing import futures


class MockFutureFactoryTests(TestCase):
    mock_future_factory = futures.MockFutureFactory()

    def test_uses_mock_spec(self) -> None:
        mock_future = self.mock_future_factory.with_result("foo")
        with self.assertRaises(AttributeError):
            mock_future.probably_not_a_valid_attribute

    def test_with_result(self) -> None:
        result = "foo"
        mock_future = self.mock_future_factory.with_result(result)
        self.assertIs(mock_future.result(), result)
        self.assertEqual(mock_future.exception(), None)

    def test_with_exception(self) -> None:
        exception = Exception()
        mock_future = self.mock_future_factory.with_exception(exception)
        self.assertIs(mock_future.exception(), exception)
        self.assertEqual(mock_future.result(), None)
