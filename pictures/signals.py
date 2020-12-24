from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed
from allauth.account.models import EmailAddress
from pictures.models import Profile, Images
from taggit.models import Tag
import random

# to prevent errors in case a username for a user was blank, generate a random username in the form of: user1234567890
@receiver(pre_save, sender=Profile, dispatch_uid="set_username_of_empty_profile_username")
def set_username(sender, instance, **kwargs):
    if not instance.username:
        rand = random.getrandbits(64)
        username = "user" + str(rand)
        while Profile.objects.filter(username=username):
            rand = random.getrandbits(64)
            username = "user" + str(rand)
        instance.username = username


# after editing a profile update the search vector with new instances
@receiver(post_save, sender=Profile)
def update_search_vector_profile(sender, instance, **kwargs):
    Profile.objects.filter(pk=instance.pk).update(
        sv=SearchVector("username", "first_name", "last_name")
    )


# after saving an instance of Image, update the search vector with new instances
@receiver(post_save, sender=Images)
def update_search_vector_profile(sender, instance, **kwargs):
    Images.objects.filter(pk=instance.pk).update(sv=SearchVector("description"))


# when a new tag is created remove spaces from the tag and convert to lowercase
@receiver(post_save, sender=Tag)
def update_tag_name(sender, instance, **kwargs):
    instance.name = instance.name.replace(" ", "").lower()
