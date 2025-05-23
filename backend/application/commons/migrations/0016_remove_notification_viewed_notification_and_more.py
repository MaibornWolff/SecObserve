# Generated by Django 5.1.8 on 2025-04-15 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0015_settings_exploit_information_max_age_years_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="notification_viewed",
                    name="notification",
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="notification_viewed",
                    name="user",
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="Notification",
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="Notification_Viewed",
                ),
            ],
            database_operations=[],
        ),
    ]
