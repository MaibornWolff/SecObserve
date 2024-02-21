import logging

from django.db import migrations

logger = logging.getLogger("secobserve.migration")


def initialize_vulnerabilities(apps, schema_editor):
    Observation = apps.get_model("core", "Observation")
    Vulnerability = apps.get_model("vex", "Vulnerability")
    for observation in Observation.objects.exclude(vulnerability_id=""):
        try:
            vulnerability = Vulnerability.objects.get(name=observation.vulnerability_id)
            if len(vulnerability.description) < len(observation.description):
                vulnerability.description = observation.description
            if len(vulnerability.recommendation) < len(observation.recommendation):
                vulnerability.recommendation = observation.recommendation
            vulnerability.save()
        except Exception:
            vulnerability = Vulnerability(
                name=observation.vulnerability_id,
                description=observation.description,
                recommendation=observation.recommendation,
            )
            vulnerability.save()


class Migration(migrations.Migration):
    dependencies = [
        ("vex", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(initialize_vulnerabilities),
    ]
