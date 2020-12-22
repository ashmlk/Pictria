# Generated by Django 3.0 on 2020-12-20 20:08

from django.db import migrations, models
import django_uuid_upload
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0017_auto_20201220_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, upload_to=functools.partial(django_uuid_upload._upload_to_uuid_impl, *(), **{'make_dir': False, 'path': 'media/users_images/', 'remove_qs': True})),
        ),
    ]