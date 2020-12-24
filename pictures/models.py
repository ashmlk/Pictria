from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, UserManager
from taggit.models import Tag
from django.utils import timezone
from django.urls import reverse
from django.core.validators import (
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast
from django.template.defaultfilters import slugify
import uuid, math, secrets, datetime, pytz, io, string
from django_uuid_upload import upload_to_uuid
from math import log
from dateutil import tz
import PIL
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from hashids import Hashids
from taggit_selectize.managers import TaggableManager
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
import django.contrib.postgres.search as pg_search
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.db.models.functions import Greatest
from collections import Counter
from itertools import chain
from django.conf import settings


hashedId_user = Hashids(
    salt="WIORUNVWinosf0940vwiev w09rhw09 wb bvwerEFUBV", min_length=12
)
hashedId_image = Hashids(
    salt="rervehr0 erOUBO80h BP89pbh smdUB3498 IUBubdevwerv", min_length=12
)
hashedId_image_class = Hashids(
    salt="evero OIBOB80h0h obsdsdSFBV030 OOS9jfsv", min_length=12
)


class ProfileManager(UserManager):
    def search(self, search_text):

        search_text = search_text.strip()
        qs = (
            self.get_queryset()
            .annotate(
                trigram=Greatest(
                    TrigramSimilarity("username", search_text),
                    TrigramSimilarity("first_name", search_text),
                    TrigramSimilarity("last_name", search_text),
                )
            )
            .filter(
                (Q(is_active=True))
                & (  # only return active users
                    Q(username__unaccent__trigram_similar=search_text)
                    | Q(last_name__unaccent__trigram_similar=search_text)
                    | Q(first_name__unaccent__trigram_similar=search_text)
                ),
                trigram__gte=0.03,
            )
            .exclude(is_superuser=True)
            .order_by("trigram")  # do show superusers (admins) on search
        )
        return qs


class ImagesManager(models.Manager):
    def search(self, search_text):

        search_vectors = SearchVector("description", weight="A", config="english")
        search_query = SearchQuery(search_text, config="english")

        search_rank = SearchRank(search_vectors, search_query)

        trigram = (
            TrigramSimilarity("description", search_text)
            + (TrigramSimilarity("tags__name", search_text))
            + (TrigramSimilarity("author__username", search_text))
            + (TrigramSimilarity("author__last_name", search_text))
            + (TrigramSimilarity("author__first_name", search_text))
        )

        relevent_tags = (
            Tag.objects.annotate(trigram=TrigramSimilarity("name", search_text))
            .filter(trigram__gte=0.7)
            .order_by("-trigram")
        )

        qs = (
            self.get_queryset()
            .select_related("author")
            .annotate(
                rank=search_rank,
                trigram=trigram,
                bs=Greatest("rank", "trigram"),
                trigram_author_username=TrigramSimilarity(
                    "author__username", search_text
                ),
                trigram_author_last_name=TrigramSimilarity(
                    "author__last_name", search_text
                ),
                trigram_author_first_name=TrigramSimilarity(
                    "author__first_name", search_text
                ),
            )
            .filter(
                (
                    Q(sv=search_query)
                    | Q(bs__gte=0.03)
                    | Q(trigram__gte=0.03)
                    | Q(rank__gte=0.15)
                    | Q(trigram_author_username__gte=0.3)
                    | Q(trigram_author_last_name__gte=0.5)
                    | Q(trigram_author_first_name__gte=0.8)
                    | Q(tags__in=relevent_tags)
                )
                & (Q(parent_image=None))
            )
            .order_by("-bs")
            .distinct()
        )
        return qs

    def get_top_tags(self):

        time_threshold = timezone.now() - datetime.timedelta(days=7)
        qs = self.get_queryset().filter(
            parent_image=None, last_edited__gte=time_threshold
        )
        tags = Images.tags.most_common(extra_filters={"images__in": qs})[:15]
        return tags

    def get_top(self):

        time_threshold = timezone.now() - datetime.timedelta(days=7)
        qs = list(
            self.get_queryset()
            .filter(last_edited__gte=time_threshold)
            .annotate(like_count=Count("likes"))
            .values_list("id", flat=True)
            .order_by("like_count")
        )
        return qs

    def get_most_viewed(self):

        time_threshold = timezone.now() - datetime.timedelta(days=10)
        qs = list(
            self.get_queryset()
            .filter(last_edited__gte=time_threshold)
            .annotate(view_count=Count("views"))
            .values_list("id", flat=True)
            .order_by("view_count")
        )
        return qs

    def get_tag_images(self, tag):

        qs = (
            self.get_queryset()
            .select_related("author")
            .filter(tags=tag)
            .order_by("-last_edited")
        )
        if qs != None:
            qs = qs.values_list("id", flat=True)
        return qs


class SearchLogManager(models.Manager):
    def related_terms(self, term):

        search_vectors = SearchVector("text", weight="A", config="english")

        similarity = TrigramSimilarity("text", term)

        search_query = SearchQuery(term, config="english")

        search_rank = SearchRank(search_vectors, search_query)

        qs = (
            self.get_queryset()
            .filter(~Q(text__iexact=term))
            .annotate(rank=search_rank, trigram=similarity)
            .filter(Q(rank__gte=0.2) | Q(trigram__gte=0.1))
            .annotate(count=Count("profile_id"))
            .order_by("-rank", "count", "-timestamp")
        )

        return qs


class Profile(AbstractUser):

    bio = models.TextField()
    profile_image = models.ImageField(
        upload_to=upload_to_uuid("profile_image/"), blank=True
    )
    save_searches = models.BooleanField(
        default=True, blank=True
    )  # boolean field to specify is user wants search results to be saved or not
    favorite_tags = models.ManyToManyField(Tag, related_name="favorite_tags")
    sv = pg_search.SearchVectorField(null=True)

    objects = ProfileManager()

    class Meta:
        indexes = [GinIndex(fields=["sv"], name="search_idx_user")]

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse("view-profile", kwargs={"username": self.username})

    def get_image_count_text(self):

        image_count = self.images.count()
        if image_count == 0 or image_count != 1:
            return "Images"
        if image_count <= 1:
            return "Image"

    def get_hashed_id(self):

        return hashedId_user.encode(self.id)

    def get_image_url(self):
        if not bool(self.profile_image):
            link = (
                "https://avatars.dicebear.com/api/avataaars/"
                + self.get_hashed_id()
                + ".svg?"
            )  # get user avatar if user image is null (DiceBear API)
        else:
            link = "{0}".format(
                self.profile_image.url
            )  # MEDIA_URL  can change based on production or development server
        return link


"""
All model instance with the prefix Unsplash are for demonstration purposes and the end user does not
intract with any of these models. This models are created using UnsplashAPI dataset 
to create examples for and demo
"""


class SearchLog(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="searches", null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(db_index=True)

    objects = SearchLogManager()

    def __str__(self):
        return self.text


# Unsplash models for Unsplash dataset
class UnsplashPhotos(models.Model):

    photo_id = models.CharField(
        max_length=255, unique=True, null=False, primary_key=True
    )
    photo_url = models.CharField(max_length=255, null=True)
    photo_image_url = models.CharField(max_length=255, null=True)
    photo_submitted_at = models.DateTimeField(auto_now=True)
    photo_featured = models.BooleanField(default=True, blank=True)
    photo_description = models.TextField()
    photographer_username = models.CharField(max_length=255, null=True)
    photographer_first_name = models.CharField(max_length=255, null=True)
    photographer_last_name = models.CharField(max_length=255, null=True)
    photo_location_name = models.CharField(max_length=255, null=True)
    photo_location_country = models.CharField(max_length=255, null=True)
    photo_location_city = models.CharField(max_length=255, null=True)
    ai_description = models.CharField(max_length=255, null=True)
    ai_primary_landmark_name = models.CharField(max_length=255, null=True)


class UnsplashKeywords(models.Model):
    photo = models.ForeignKey(UnsplashPhotos, on_delete=models.CASCADE)
    keyword = models.TextField()
    ai_service_1_confidence = models.FloatField()
    ai_service_2_confidence = models.FloatField()
    suggested_by_user = models.BooleanField(default=True, blank=True)


class UnsplashCollections(models.Model):
    photo = models.ForeignKey(
        UnsplashPhotos, on_delete=models.CASCADE, related_name="collections"
    )
    collection_title = models.TextField(null=True)
    photo_collected_at = models.DateTimeField(auto_now_add=True)


# this is the main Images model that user are able to interact with
class Images(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="images")
    date_added = models.DateTimeField(auto_now_add=True)
    guid_url = models.CharField(max_length=255, unique=True, null=True)
    description = models.TextField(validators=[MaxLengthValidator(180)])
    last_edited = models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    is_collection = models.BooleanField(null=True, blank=True, default=False)
    parent_image = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child_images",
        null=True,
        blank=True,
    )
    likes = models.ManyToManyField(Profile, blank=True, related_name="likes")
    views = models.ManyToManyField(Profile, blank=True, related_name="views")
    image_photo = models.ImageField(
        upload_to=upload_to_uuid("users_images/"), blank=True
    )
    # this is for demo purposes inly, remove ForeignKey relationship with UnsplashPhoto on real production
    unsplash_photo = models.ForeignKey(
        UnsplashPhotos,
        on_delete=models.CASCADE,
        null=True,
        related_name="unsplash_image",
    )
    sv = pg_search.SearchVectorField(null=True)

    objects = ImagesManager()

    class Meta:
        indexes = [GinIndex(fields=["sv"], name="search_idx_images")]

    def save(self, *args, **kwargs):
        if (
            self.pk is None
        ):  # image compression is done to avoid overloading server with large images
            try:
                MAX_WIDTH = 1080
                MAX_HEIGHT = 1350
                img = Image.open(self.image_photo)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                exif = None
                if "exif" in img.info:
                    exif = img.info["exif"]
                ratio = min(MAX_WIDTH / img.size[0], MAX_HEIGHT / img.size[1])
                if img.size[0] > MAX_WIDTH or img.size[1] > MAX_HEIGHT:
                    img = img.resize(
                        (int(img.size[0] * ratio), int(img.size[1] * ratio)),
                        PIL.Image.ANTIALIAS,
                    )
                elif self.parent_image != None:
                    pimg = Image.open(self.parent_image.image_photo)
                    if pimg.mode in ("RGBA", "P"):
                        pimg = pimg.convert("RGB")
                    img = img.resize((pimg.size[0], pimg.size[1]), PIL.Image.ANTIALIAS)
                else:
                    img = img.resize((img.size[0], img.size[1]), PIL.Image.ANTIALIAS)
                output = io.BytesIO()
                if exif:
                    img.save(
                        output, format="JPEG", exif=exif, quality=80
                    )  # images will all be converted to JPEG  keeping quality of 80
                else:
                    img.save(output, format="JPEG", quality=80)
                output.seek(0)
                self.image_photo = InMemoryUploadedFile(
                    output,
                    "ImageField",
                    "%s.jpg" % self.image_photo.name,
                    "image/jpeg",
                    output.getbuffer().nbytes,
                    None,
                )
            except Exception as e:
                print(e)
        self.guid_url = secrets.token_urlsafe(8)
        super(Images, self).save(*args, **kwargs)

    def get_hashed_id(self):
        return hashedId_image.encode(self.id)

    def get_class_hashed_id(self):
        return hashedId_image_class.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.date_added
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"

    # The following methods are only for demo purposes and images created by real users will not use these
    # Methods are used to construct Images and data from relative UnsplashPhotos object

    # method to return a list of all collection titles image with a relationship to UnsplashPhotos
    def get_unsplash_collection_title(self):
        if self.unsplash_photo != None:
            collection_objs = self.unsplash_photo.collections.all()
            if collection_objs != None:
                return [c.collection_title.strip().lower() for c in collection_objs][
                    :10
                ]
            return None

    # returns a dict object of unsplash photo fields if image has a relationship with unsplash object
    def get_unsplash_image(self):
        if self.unsplash_photo != None:
            p = self.unsplash_photo
            return {
                "photo_url": p.photo_url,
                "photo_image_url": p.photo_image_url,
                "photo_submitted_at": p.photo_submitted_at,
                "photo_featured": p.photo_featured,
                "photo_description": p.photo_description,
                "photographer_first_name": p.photographer_first_name,
                "photographer_last_name": p.photographer_last_name,
                "location_city": p.photo_location_city,
                "location_name": p.photo_location_name,
                "location_country": p.photo_location_country,
                "ai_description": p.ai_description,
                "ai_landmark": p.ai_primary_landmark_name,
            }
        else:
            return None


class Bookmark(models.Model):

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="bookmarks"
    )
    image = models.ForeignKey(
        Images, on_delete=models.CASCADE, related_name="bookmarked"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.id + " --- " + self.profile.id
