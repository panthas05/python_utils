from django import forms as django_forms

from unittest import TestCase

from . import django_test_case
from src.django import forms


class DummyEmailForm(django_forms.Form):
    email = django_forms.EmailField()


class ExtractFormErrorsTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    def test_functionality(self) -> None:
        form = DummyEmailForm({"email": "Not an email"})
        # accessing errors property forces call to is_valid
        errors = forms.extract_form_errors(form)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("email: "))
