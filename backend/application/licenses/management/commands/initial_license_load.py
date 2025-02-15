import logging
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from application.licenses.models import License, License_Group, License_Policy

logger = logging.getLogger("secobserve.licenses")


class Command(BaseCommand):

    help = "Initial load of licenses, license groups and license policies."

    def handle(self, *args: Any, **options: Any) -> None:
        licenses_exist = License.objects.exists()
        license_groups_exist = License_Group.objects.exists()
        license_policies_exist = License_Policy.objects.exists()

        if (
            not licenses_exist
            and not license_groups_exist
            and not license_policies_exist
        ):
            logger.info(
                "Importing initial licenses, license groups and license policies..."
            )
            call_command("loaddata", "application/licenses/fixtures/initial_data.json")
