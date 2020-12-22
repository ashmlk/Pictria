release: python manage.py migrate --settings=pictria.settings.production
web: gunicorn pictria.wsgi:application --env DJANGO_SETTINGS_MODULE='pictria.settings.production' --log-file -
worker: celery -A pictria worker -E -l info
celery_beat: celery -A pictria beat --loglevel=info