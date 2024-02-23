# Generated by Django 4.2.10 on 2024-02-23 03:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0031_observation_issue_tracker_issue_closed_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CSAF",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vulnerability_name", models.CharField(blank=True, max_length=255)),
                ("document_base_id", models.CharField(max_length=36, unique=True)),
                ("document_id", models.CharField(max_length=255)),
                (
                    "version",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(999999),
                        ]
                    ),
                ),
                ("content_hash", models.CharField(blank=True, max_length=256)),
                ("title", models.CharField(max_length=255)),
                (
                    "tracking_initial_release_date",
                    models.DateTimeField(auto_now_add=True),
                ),
                ("tracking_current_release_date", models.DateTimeField(auto_now=True)),
                (
                    "tracking_status",
                    models.CharField(
                        choices=[
                            ("draft", "draft"),
                            ("final", "final"),
                            ("interim", "interim"),
                        ],
                        max_length=16,
                    ),
                ),
                ("publisher_name", models.CharField(max_length=255)),
                (
                    "publisher_category",
                    models.CharField(
                        choices=[
                            ("coordinator", "coordinator"),
                            ("discoverer", "discoverer"),
                            ("other", "other"),
                            ("translator", "translator"),
                            ("user", "user"),
                            ("vendor", "vendor"),
                        ],
                        max_length=16,
                    ),
                ),
                ("publisher_namespace", models.CharField(max_length=255)),
                (
                    "product",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Vulnerability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, max_length=2048)),
                ("recommendation", models.TextField(blank=True, max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name="OpenVEX",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vulnerability_name", models.CharField(blank=True, max_length=255)),
                ("document_base_id", models.CharField(max_length=36, unique=True)),
                ("document_id", models.CharField(max_length=255)),
                (
                    "version",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(999999),
                        ]
                    ),
                ),
                ("content_hash", models.CharField(blank=True, max_length=256)),
                ("author", models.CharField(max_length=255)),
                ("role", models.CharField(blank=True, max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CSAF_Revision",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("revision_date", models.DateTimeField()),
                (
                    "revision_version",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(999999),
                        ]
                    ),
                ),
                ("summary", models.TextField(max_length=255)),
                (
                    "csaf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vex.csaf"
                    ),
                ),
            ],
        ),
    ]
