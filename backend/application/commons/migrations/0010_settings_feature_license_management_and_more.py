# Generated by Django 5.1.2 on 2024-10-15 10:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0009_settings_password_validator_attribute_similarity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="feature_license_management",
            field=models.BooleanField(
                default=True, help_text="Enable license management"
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="license_import_crontab_hour",
            field=models.IntegerField(
                default=1,
                help_text="Hour crontab expression for importing licenses (UTC)",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(23),
                ],
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="license_import_crontab_minute",
            field=models.IntegerField(
                default=30,
                help_text="Minute crontab expression for importing licenses",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(59),
                ],
            ),
        ),
    ]