# Generated by Django 4.2.9 on 2024-01-05 18:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_observation_origin_cloud_account_subscription_project_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="notification_slack_webhook",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]