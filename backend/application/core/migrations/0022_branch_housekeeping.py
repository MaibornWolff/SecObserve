# Generated by Django 4.2.3 on 2023-07-28 15:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0021_observation_issue_tracker_jira_initial_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="branch",
            name="housekeeping_protect",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="branch",
            name="last_import",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="repository_branch_housekeeping_active",
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="repository_branch_housekeeping_exempt_branches",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="repository_branch_housekeeping_keep_inactive_days",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999999),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="observation",
            name="branch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="core.branch"
            ),
        ),
    ]