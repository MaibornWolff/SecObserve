# Generated by Django 5.1.2 on 2024-10-12 17:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "commons",
            "0008_remove_settings_background_epss_import_crontab_hours_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="password_validator_attribute_similarity",
            field=models.BooleanField(
                default=True,
                help_text="Validates that the password is sufficiently different from certain attributes of the user.",
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="password_validator_common_passwords",
            field=models.BooleanField(
                default=True,
                help_text="Validates that the password is not a common password.",
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="password_validator_minimum_length",
            field=models.IntegerField(
                default=8,
                help_text="Validates that the password is of a minimum length.",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(4096),
                ],
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="password_validator_not_numeric",
            field=models.BooleanField(
                default=True,
                help_text="Validate that the password is not entirely numeric.",
            ),
        ),
    ]
