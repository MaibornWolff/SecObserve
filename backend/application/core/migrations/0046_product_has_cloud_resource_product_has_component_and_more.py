# Generated by Django 5.0.8 on 2024-08-21 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0045_populate_observation_purl_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="has_cloud_resource",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="has_component",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="has_docker_image",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="has_endpoint",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="has_potential_duplicates",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="has_source",
            field=models.BooleanField(default=False),
        ),
    ]
