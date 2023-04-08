# Generated by Django 3.2.16 on 2022-11-17 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rule",
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
                ("scanner_prefix", models.CharField(blank=True, max_length=255)),
                ("title", models.CharField(max_length=255)),
                (
                    "new_parser_severity",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Unkown", "Unkown"),
                            ("None", "None"),
                            ("Low", "Low"),
                            ("Medium", "Medium"),
                            ("High", "High"),
                            ("Critical", "Critical"),
                        ],
                        max_length=12,
                    ),
                ),
                (
                    "new_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Open", "Open"),
                            ("Resolved", "Resolved"),
                            ("Duplicate", "Duplicate"),
                            ("False positive", "False positive"),
                            ("In review", "In review"),
                            ("Not affected", "Not affected"),
                            ("Risk accepted", "Risk accepted"),
                        ],
                        max_length=16,
                    ),
                ),
                (
                    "parser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.parser"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.product",
                    ),
                ),
            ],
        ),
    ]
