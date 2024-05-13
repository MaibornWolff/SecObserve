# Generated by Django 5.0.6 on 2024-05-13 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vex", "0005_alter_vex_counter_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="VEX_Document",
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
                (
                    "type",
                    models.CharField(
                        choices=[("csaf", "csaf"), ("openvex", "openvex")],
                        max_length=16,
                    ),
                ),
                ("document_id", models.CharField(max_length=255)),
                ("version", models.CharField(max_length=255)),
                ("current_release_date", models.DateTimeField()),
                ("initial_release_date", models.DateTimeField()),
                ("author", models.CharField(max_length=255)),
                ("role", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "unique_together": {("document_id", "author")},
            },
        ),
        migrations.CreateModel(
            name="VEX_Statement",
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
                ("vulnerability_id", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=24)),
                (
                    "justification",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("component_not_present", "component_not_present"),
                            (
                                "vulnerable_code_not_present",
                                "vulnerable_code_not_present",
                            ),
                            (
                                "vulnerable_code_cannot_be_controlled_by_adversary",
                                "vulnerable_code_cannot_be_controlled_by_adversary",
                            ),
                            (
                                "vulnerable_code_not_in_execute_path",
                                "vulnerable_code_not_in_execute_path",
                            ),
                            (
                                "inline_mitigations_already_exist",
                                "inline_mitigations_already_exist",
                            ),
                        ],
                        max_length=64,
                    ),
                ),
                ("impact", models.CharField(blank=True, max_length=255)),
                ("remediation", models.CharField(blank=True, max_length=255)),
                ("product_id", models.CharField(max_length=255)),
                ("product_purl", models.CharField(blank=True, max_length=255)),
                ("product_cpe23", models.CharField(blank=True, max_length=255)),
                ("component_id", models.CharField(blank=True, max_length=255)),
                ("component_purl", models.CharField(blank=True, max_length=255)),
                ("component_cpe23", models.CharField(blank=True, max_length=255)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statements",
                        to="vex.vex_document",
                    ),
                ),
            ],
        ),
    ]
