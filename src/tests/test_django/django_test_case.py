import django
from django.conf import settings

from unittest import TestCase
import os

_django_set_up_done = False


class DjangoDependentTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        global _django_set_up_done
        if not _django_set_up_done:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings")
            django.setup()
            _django_set_up_done = True
        return super().__init__(*args, **kwargs)
