import picklefield.fields  # nosec B403

# picklefield is used to store python objects in the database
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Constance",
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
                ("key", models.CharField(max_length=255, unique=True)),
                (
                    "value",
                    picklefield.fields.PickledObjectField(blank=True, editable=False, null=True),
                ),
            ],
            options={
                "verbose_name": "constance",
                "verbose_name_plural": "constances",
                "permissions": [
                    ("change_config", "Can change config"),
                    ("view_config", "Can view config"),
                ],
            },
        ),
    ]
