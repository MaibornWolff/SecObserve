# Generated by Django 4.2.2 on 2023-06-10 01:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_branch_observation_branch_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="branch",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
