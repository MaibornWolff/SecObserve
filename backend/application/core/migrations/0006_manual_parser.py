# Generated by Django 3.2.16 on 2023-01-06 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_last_observation_log_data"),
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
                    ("Unkown", "Unkown"),
                ],
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="parser",
            name="type",
            field=models.CharField(
                choices=[
                    ("SCA", "SCA"),
                    ("SAST", "SAST"),
                    ("DAST", "DAST"),
                    ("IAST", "IAST"),
                    ("Secrets", "Secrets"),
                    ("Communication", "Communication"),
                    ("Infrastructure", "Infrastructure"),
                    ("Other", "Other"),
                    ("Manual", "Manual"),
                ],
                max_length=16,
            ),
        ),
    ]