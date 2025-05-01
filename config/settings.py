import os
from pathlib import Path

from config.redis import REDIS_DJANGO_DB, REDIS_HOST, REDIS_PORT

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# Environment
ENV = "prod"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
]
INTERNAL_IPS = [
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
]

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

EXTERNAL_APPS = [
    "django_celery_beat",
]

PROJECT_APPS = [
    "experiments",
]

INSTALLED_APPS = DEFAULT_APPS + EXTERNAL_APPS + PROJECT_APPS


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = "static/"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database settings with support for a replica DB
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# Pool documentation: https://www.psycopg.org/psycopg3/docs/api/pool.html#psycopg_pool.ConnectionPool
DEFAULT_DB = "default"
DATABASES = {
    DEFAULT_DB: {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("EXPERIMENTS_DB_NAME", "experimentsdb"),
        "USER": os.environ.get("EXPERIMENTS_DB_USER", "postgres"),
        "PASSWORD": os.environ.get("EXPERIMENTS_DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("EXPERIMENTS_DB_HOST", "localhost"),
        "PORT": os.environ.get("EXPERIMENTS_DB_PORT", "5432"),
    },
}

# LOGGING
# https://docs.djangoproject.com/en/stable/ref/settings/#logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{asctime}: {levelname}/{threadName}][{filename:s}:L{lineno}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": False,
            "level": "INFO",
        },
    },
}

# Django backend cache using Redis
DEFAULT_CACHE_TIMEOUT = 60 * 60 * 24  # 1 day
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DJANGO_DB}",
        "TIMEOUT": DEFAULT_CACHE_TIMEOUT,
        "KEY_PREFIX": "django",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
