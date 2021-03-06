# Generated by Django 3.0 on 2020-12-19 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("pictures", "0012_unsplashcollections_collection_title")]

    operations = [
        migrations.AlterField(
            model_name="unsplashcollections",
            name="photo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collections",
                to="pictures.UnsplashPhotos",
            ),
        )
    ]
