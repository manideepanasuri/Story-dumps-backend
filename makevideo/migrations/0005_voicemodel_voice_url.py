# Generated by Django 5.2.2 on 2025-06-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("makevideo", "0004_backgroundmodel_voicemodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="voicemodel",
            name="voice_url",
            field=models.URLField(default=""),
        ),
    ]
