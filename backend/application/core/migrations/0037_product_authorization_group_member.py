# Generated by Django 4.2.11 on 2024-03-27 19:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access_control", "0008_user_oidc_groups_hash_authorization_group"),
        ("core", "0036_observation_log_approval_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product_Authorization_Group_Member",
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
                    "role",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "authorization_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="access_control.authorization_group",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.product"
                    ),
                ),
            ],
            options={
                "unique_together": {("product", "authorization_group")},
            },
        ),
    ]