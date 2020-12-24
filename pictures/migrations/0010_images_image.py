# Generated by Django 3.0 on 2020-12-19 03:15

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [("pictures", "0009_remove_images_image")]

    operations = [
        migrations.AddField(
            model_name="images",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=functools.partial(
                    django_uuid_upload._upload_to_uuid_impl,
                    *(),
                    **{"make_dir": False, "path": "users_images/", "remove_qs": True}
                ),
            ),
        )
    ]
