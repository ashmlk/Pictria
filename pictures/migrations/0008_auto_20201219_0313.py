# Generated by Django 3.0 on 2020-12-19 03:13

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [("pictures", "0007_auto_20201219_0310")]

    operations = [
        migrations.AlterField(
            model_name="images",
            name="image",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=functools.partial(
                    django_uuid_upload._upload_to_uuid_impl,
                    *(),
                    **{"make_dir": False, "path": "media/images/", "remove_qs": True}
                ),
            ),
        )
    ]
