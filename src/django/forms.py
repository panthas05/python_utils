from django import forms
from django.core.files.uploadedfile import UploadedFile

from typing import Any


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(
        self,
        data: Any,
        initial: Any | None = None,
    ) -> UploadedFile | list[UploadedFile]:
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

    def run_validators(
        self,
        value: Any,
    ) -> None:
        single_run_validators = super().run_validators
        if isinstance(value, (list, tuple)):
            for f in value:
                single_run_validators(f)
        else:
            single_run_validators(value)


DjangoForm = forms.Form | forms.ModelForm


def extract_form_errors(form: DjangoForm) -> list[str]:
    return [f"{k}: {v[0]}" for k, v in form.errors.items()]
