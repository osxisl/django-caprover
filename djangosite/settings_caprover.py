import os

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

from .settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("CR_SECRET_KEY") or ImproperlyConfigured("CR_SECRET_KEY not set")

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

# allowed hosts get parsed from a comma-separated list
hosts = os.environ.get("CR_HOSTS") or ImproperlyConfigured("CR_HOSTS not set")
try:
    ALLOWED_HOSTS = hosts.split(",")
except:
    raise ImproperlyConfigured("CR_HOSTS could not be parsed")


# Database
if os.environ.get("CR_USESQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / 'db/db.sqlite3'),
        }
    }
else:
    name = os.environ.get("CR_DB_NAME") or ImproperlyConfigured("CR_DB_NAME not set")
    user = os.environ.get("CR_DB_USER") or ImproperlyConfigured("CR_DB_USER not set")
    password = os.environ.get("CR_DB_PASSWORD") or ImproperlyConfigured("CR_DB_PASSWORD not set")
    host = os.environ.get("CR_DB_HOST") or ImproperlyConfigured("CR_DB_HOST not set")
    port = os.environ.get("CR_DB_PORT") or ImproperlyConfigured("CR_DB_PORT not set")

    DATABASES = {
        "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
        }
    }


