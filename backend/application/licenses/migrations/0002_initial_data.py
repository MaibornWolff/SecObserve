from django.db.migrations import Migration, RunPython


class Migration(Migration):
    # This migration exists for historical reasons in the development process and is a no-op on purpose.

    dependencies = [
        ("licenses", "0001_initial"),
    ]

    operations = [
        RunPython(code=RunPython.noop, reverse_code=RunPython.noop),
    ]
