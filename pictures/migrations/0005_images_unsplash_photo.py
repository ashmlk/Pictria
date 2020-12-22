# Generated by Django 3.0 on 2020-12-19 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0004_unsplashcollections_unsplashkeywords_unsplashphotos'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='unsplash_photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unsplash_image', to='pictures.UnsplashPhotos'),
        ),
    ]
