# Generated by Django 5.0.6 on 2024-06-28 12:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0005_settings_feature_general_rules_need_approval"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="risk_acceptance_expiry_crontab_hours",
            field=models.IntegerField(
                default=1,
                help_text="Hours crontab expression for checking risk acceptance expiry (UTC)",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(23),
                ],
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="risk_acceptance_expiry_crontab_minutes",
            field=models.IntegerField(
                default=0,
                help_text="Minutes crontab expression for checking risk acceptance expiry",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(59),
                ],
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="risk_acceptance_expiry_days",
            field=models.IntegerField(
                default=30,
                help_text="Days before risk acceptance expires, 0 means no expiry",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999999),
                ],
            ),
        ),
    ]
