# Generated by Django 3.2.17 on 2023-02-13 10:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rules", "0005_uniqueness"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rule",
            name="new_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Open", "Open"),
                    ("Resolved", "Resolved"),
                    ("Duplicate", "Duplicate"),
                    ("False positive", "False positive"),
                    ("In review", "In review"),
                    ("Not affected", "Not affected"),
                    ("Not security", "Not security"),
                    ("Risk accepted", "Risk accepted"),
                ],
                max_length=16,
            ),
        ),
    ]
