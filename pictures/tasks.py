"""
Scheduled tasks running on Celery beat
Min 1 workers required on heroku for running tasks per scheduled.
Currently there are no unscheduled tasks - minimizing dyno usage on Heroku
"""

from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from pictures.models import Images
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import datetime
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)

# get the top tags for all images every one hour- scheduled tasks via Celery Beat
@shared_task(bind=True)
def get_top_tags(self):
    top_tags = Images.objects.get_top_tags()
    cache.set("images_top_tags", top_tags, 3600)


# get the top images based on number of likes every one hour
@shared_task(bind=True)
def get_top_images(self):
    top_images = Images.objects.get_top()
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(top_images)])
    top_images = Images.objects.all().order_by(-preserved)
    cache.set("images_top_images", top_images, 3600)


# get the latest images every 10 minutes
@shared_task(bind=True)
def get_latest_images(self):
    latest_images = Images.objects.all().order_by("-last_edited")
    cache.set("images_all_latest_images", latest_images, 600)


# get the top viewed images based on the number of views
@shared_task(bind=True)
def get_top_viewed_images(self):
    top_viewed_images = Images.objects.get_most_viewed()
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(top_viewed_images)]
    )
    top_viewed_images = (
        Images.objects.all().filter(parent_image=None).order_by(-preserved)
    )
    cache.set("images_top_viewed_images", top_viewed_images, 7200)
