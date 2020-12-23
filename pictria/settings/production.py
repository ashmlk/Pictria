from pictria.settings.common import *
import os
from urllib.parse import urlparse
import django_heroku
import dj_database_url


# production environment settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False

ALLOWED_HOSTS = ['pictria.herokuapp.com']

CACHES = {
    'default': {
        'BACKEND': "redis_cache.RedisCache",
        'LOCATION': os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379'), 
        "OPTIONS": {
            'DB': 0,
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}
SITE_ID = 2

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_connections": 2,
}

SECURE_SSL_REDIRECT = True

DEBUG_PROPAGATE_EXCEPTIONS = True

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static-root')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

AWS_S3_REGION_NAME = 'us-east-2'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
DEFAULT_FILE_STORAGE = 'pictria.storage_backends.MediaStorage'
