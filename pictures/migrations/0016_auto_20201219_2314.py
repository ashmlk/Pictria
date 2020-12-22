# Generated by Django 3.0 on 2020-12-19 23:14

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import pictures.models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0015_auto_20201219_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', pictures.models.ProfileManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='images',
            name='collection',
        ),
        migrations.AddField(
            model_name='images',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='views', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='searchlog',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='searches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=django.contrib.postgres.indexes.GinIndex(fields=['sv'], name='search_idx_user'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked', to='pictures.Images'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]