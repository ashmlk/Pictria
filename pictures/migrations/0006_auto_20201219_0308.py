# Generated by Django 3.0 on 2020-12-19 03:08

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0005_images_unsplash_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(null=True, upload_to=functools.partial(django_uuid_upload._upload_to_uuid_impl, *(), **{'make_dir': False, 'path': 'media/images/', 'remove_qs': True}), verbose_name='Image'),
        ),
    ]