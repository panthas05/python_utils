import django
from django.conf import settings

import os
from typing import Any
from unittest import TestCase

_django_set_up_done = False


class DjangoDependentTestCase(TestCase):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        global _django_set_up_done
        if not _django_set_up_done:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings")
            django.setup()
            _django_set_up_done = True
        return super().__init__(*args, **kwargs)
