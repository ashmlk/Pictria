from pictria.settings.common import *
import os

# settings for development environment

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 1

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = "/static/"
MEDIA_DIRS = [os.path.join(BASE_DIR, "media")]

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "live-static", "static-root")
# Static files (CSS, JavaScript, Images)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
