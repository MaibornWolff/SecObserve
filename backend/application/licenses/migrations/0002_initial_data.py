from django.core.management import call_command
from django.db import migrations


def load_initial_data(apps, schema_editor):
    call_command("loaddata", "application/licenses/migrations/data/initial_data.json")


def reverse(apps, schema_editor):
    pass  # nosemgrep
    # This is a no-op on purpose because we can't reverse loading initial data


class Migration(migrations.Migration):

    dependencies = [
        ("licenses", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse),
    ]
