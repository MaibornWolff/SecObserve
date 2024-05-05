# Generated by Django 4.2.11 on 2024-04-27 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0003_migrate_settings_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="feature_disable_user_login",
            field=models.BooleanField(default=False, help_text="Disable user login"),
        ),
    ]
