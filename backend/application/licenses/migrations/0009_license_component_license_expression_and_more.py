# Generated by Django 5.1.3 on 2024-11-26 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("licenses", "0008_alter_license_policy_item_license_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="license_component",
            name="license_expression",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="license_policy_item",
            name="license_expression",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
