# Generated by Django 3.2.16 on 2022-11-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="ms_teams_webhook",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
