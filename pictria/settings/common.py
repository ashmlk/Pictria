"""
Common settings shared between production and development 
environments. 
"""

import os
from django.urls import reverse_lazy
from celery.schedules import crontab
import dj_database_url

SECRET_KEY = "9^d+z5dna(^dhrqa$bjhl_yl_1px1w^-)!1th8m1077ke$5@-("

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "live-static", "static-root")

MEDIA_URL = "/media/"
MEDIA_DIRS = [os.path.join(BASE_DIR, "media")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "pictures.Profile"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "pictures",
    "djutils",
    "crispy_forms",
    "taggit",
    "taggit_selectize",
    "dal",
    "dal_select2",
    "django_celery_results",
    "django_celery_beat",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "admin_honeypot",
    "whitenoise.runserver_nostatic",
    "storages",
    "sorl.thumbnail",
    "fast_pagination",
]

TAGGIT_SELECTIZE = {
    "MINIMUM_QUERY_LENGTH": 1,
    "RECOMMENDATION_LIMIT": 8,
    "PERSIST": False,
    "OPEN_ON_FOCUS": False,
    "HIDE_SELECTED": True,
    "CLOSE_AFTER_SELECT": True,
    "LOAD_THROTTLE": 100,
    "SELECT_ON_TAB": True,
    "REMOVE_BUTTON": True,
}

TAGGIT_TAGS_FROM_STRING = "taggit_selectize.utils.parse_tags"
TAGGIT_STRING_FROM_TAGS = "taggit_selectize.utils.join_tags"

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pictria.urls"

SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "pictria.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "shopify_project",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "",
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "redis_one",
    }
}

CELERY_BROKER_URL = os.environ.get("REDISTOGO_URL", "redis://127.0.0.1:6379")
CELERY_BROKER_TRANSPORT = "redis"
CELERY_RESULT_BACKEND = os.environ.get("REDISTOGO_URL", "redis://127.0.0.1:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = ("pictures.tasks",)
CELERY_BEAT_SCHEDULE = {
    "images-get-top-tags": {"task": "pictures.tasks.get_top_tags", "schedule": 1800.0},
    "images-get-top-images": {
        "task": "pictures.tasks.get_top_images",
        "schedule": 1800.0,
    },
    "images-get-latest-images": {
        "task": "pictures.tasks.get_latest_images",
        "schedule": 600.0,
    },
    "images-get-most-viewed-images": {
        "task": "pictures.tasks.get_top_viewed_images",
        "schedule": 3600.0,
    },
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "redis_one",
    }
}


# Settings for allauth login and sign up functionality
# immediately log out user on GET request ( no confirmation page )
# users will be able to sign in with both email and username
# all usernames will be converted to lowercase letters
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_VERIFICATION = "none"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGOUT_REDIRECT_URL = reverse_lazy("home")
