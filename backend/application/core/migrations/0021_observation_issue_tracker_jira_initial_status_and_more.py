# Generated by Django 4.2.3 on 2023-07-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_product_is_product_group_product_product_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="issue_tracker_jira_initial_status",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="issue_tracker_issue_type",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="issue_tracker_status_closed",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="issue_tracker_username",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="product",
            name="issue_tracker_type",
            field=models.CharField(
                blank=True,
                choices=[("GitHub", "GitHub"), ("GitLab", "GitLab"), ("Jira", "Jira")],
                max_length=12,
            ),
        ),
    ]