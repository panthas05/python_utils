from unittest import TestCase

from . import django_test_case
from src import data_cleaning


class CleanEmailTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    def test_removes_folders(self) -> None:
        self.assertEqual(data_cleaning.clean_email("foo+bish@bar.com"), "foo@bar.com")

    def test_leaves_folderless_emails_untouched(self) -> None:
        email = 'foo!"£$%^&*()_@bar.com'
        self.assertEqual(data_cleaning.clean_email(email), email)

    def test_non_email_returns_empty_string(self) -> None:
        cleaned_email = data_cleaning.clean_email("not an email")
        self.assertEqual(cleaned_email, "")
