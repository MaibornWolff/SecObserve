# Generated by Django 5.1.7 on 2025-03-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("import_observations", "0011_osv_cache_alter_parser_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="parser",
            name="sbom",
            field=models.BooleanField(default=False),
        ),
    ]
