# Generated by Django 3.0 on 2020-12-19 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("pictures", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="UnsplashPhotos",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ai_primary_landmark_confidence",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnsplashKeywords",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pictures.UnsplashPhotos",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnsplashCollections",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pictures.UnsplashPhotos",
                    ),
                ),
            ],
        ),
    ]
