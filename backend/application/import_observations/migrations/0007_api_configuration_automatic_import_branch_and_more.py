# Generated by Django 5.0.9 on 2024-09-11 12:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0049_observation_origin_kubernetes_cluster_and_more"),
        ("import_observations", "0006_parser_alter_api_configuration_parser"),
    ]

    operations = [
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_branch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="core.branch"
            ),
        ),
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_docker_image_name_tag",
            field=models.CharField(blank=True, max_length=513),
        ),
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_endpoint_url",
            field=models.CharField(blank=True, max_length=2048),
        ),
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_kubernetes_cluster",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="api_configuration",
            name="automatic_import_service",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="api_configuration",
            name="basic_auth_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="api_configuration",
            name="verify_ssl",
            field=models.BooleanField(default=False),
        ),
    ]
