# Generated by Django 3.0 on 2020-12-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pictures", "0020_auto_20201221_0518")]

    operations = [
        migrations.AlterField(
            model_name="images",
            name="is_collection",
            field=models.BooleanField(blank=True, default=False, null=True),
        )
    ]
