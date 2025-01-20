# Generated by Django 3.2.16 on 2022-12-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rules", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="rule",
            name="origin_component_name_version",
            field=models.CharField(blank=True, max_length=513),
        ),
        migrations.AddField(
            model_name="rule",
            name="origin_docker_image_name_tag",
            field=models.CharField(blank=True, max_length=513),
        ),
        migrations.AddField(
            model_name="rule",
            name="origin_endpoint_url",
            field=models.TextField(blank=True, max_length=2048),
        ),
        migrations.AddField(
            model_name="rule",
            name="origin_service_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="rule",
            name="origin_source_file",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="rule",
            name="title",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]