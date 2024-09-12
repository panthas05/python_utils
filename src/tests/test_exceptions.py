from unittest import TestCase

from src import exceptions


class PromoteBaseExceptionTests(TestCase):
    def test_returns_exception_unchanged(self) -> None:
        exception = Exception("foo")
        self.assertEqual(exceptions.promote_base_exception(exception), exception)

    def test_promotes_base_exception_to_exception(self) -> None:
        exception = BaseException()
        self.assertIsInstance(exceptions.promote_base_exception(exception), Exception)

    def test_preserves_exception_attributes(self) -> None:
        class CustomException(BaseException):
            def custom_method(self) -> str:
                return "Foo"

        exception = exceptions.promote_base_exception(CustomException())
        self.assertTrue(hasattr(exception, "custom_method"))
        self.assertEqual(exception.custom_method(), "Foo")  # type: ignore

    def test_throws_for_non_exception(self) -> None:
        self.assertRaises(
            Exception,
            exceptions.promote_base_exception,
            "A String",
        )
