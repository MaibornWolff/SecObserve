# Generated by Django 5.1.3 on 2024-11-21 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("licenses", "0007_license_component_evidence_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="license_policy_item",
            name="license_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="license_policy_items",
                to="licenses.license_group",
            ),
        ),
    ]
