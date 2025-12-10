# dummy file so django tests can run

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INSTALLED_APPS = [
    # having these two apps "installed" prevents exceptions when running mypy
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MUTEX_NAMESPACE = "blah"
