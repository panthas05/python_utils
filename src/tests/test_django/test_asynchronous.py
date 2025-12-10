from unittest import mock, TestCase

from . import django_test_case
from src.django import asynchronous


@mock.patch(
    "src.django.asynchronous.logging.send_error_email",
    autospec=True,
)
class ExtractResultsWithLoggingTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    def test_returns_results(self, mock_send_error_email):
        result = "foo"
        results = asynchronous.extract_results_with_logging([result, result, result])
        self.assertEqual(results, [result, result, result])
        mock_send_error_email.assert_not_called()

    def test_logs_exceptions(self, mock_send_error_email):
        result = "foo"
        exception = Exception("bar")
        results = asynchronous.extract_results_with_logging([result, exception])
        self.assertEqual(results, [result])
        mock_send_error_email.assert_called_once_with(exception, request=None)

    # def test_raises_when_all_exceptions(self, mock_send_error_email):
    #     exception = Exception("foo")
    #     with self.assertRaises(ExceptionGroup) as cm:
    #         results = asynchronous.extract_results_with_logging(
    #             [exception, exception, exception]
    #         )
    #         self.assertEqual(results, [])
    #     self.assertEqual(cm.exception.exceptions, (exception, exception, exception))
    #     mock_send_error_email.assert_not_called()
