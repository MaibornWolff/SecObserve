# Generated by Django 5.1.2 on 2024-10-24 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "import_observations",
            "0007_api_configuration_automatic_import_branch_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="parser",
            name="source",
            field=models.CharField(
                choices=[
                    ("API", "API"),
                    ("File", "File"),
                    ("Manual", "Manual"),
                    ("Unknown", "Unknown"),
                ],
                max_length=16,
            ),
        ),
    ]
