# Generated by Django 4.2.7 on 2023-11-08 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_branch_housekeeping"),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
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
                ("name", models.CharField(max_length=255)),
                (
                    "product",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.product"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="observation",
            name="origin_service",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.service",
            ),
        ),
        migrations.AddIndex(
            model_name="service",
            index=models.Index(fields=["name"], name="core_servic_name_2e1bf5_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="service",
            unique_together={("product", "name")},
        ),
    ]
