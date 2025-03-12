from typing import Any

import environ
from django.db.models.signals import post_save
from django.dispatch import receiver
from huey.contrib.djhuey import db_task, lock_task

from application.commons.models import Settings
from application.core.models import Product
from application.core.services.security_gate import check_security_gate
from application.epss.models import Exploit_Information
from application.epss.services.cvss_bt import (
    apply_exploit_information_observations,
    import_cvss_bt,
)


@receiver(post_save, sender=Settings)
def settings_post_save(  # pylint: disable=unused-argument
    sender: Any, instance: Settings, created: bool, **kwargs: Any
) -> None:

    print("--- settings_post_save ---")

    # parameters are needed according to Django documentation
    env = environ.Env()
    if not env.bool("SO_UNITTESTS", False):

        print("--- not SO_UNITTESTS ---")

        settings_post_save_task(instance, created)


@db_task()
@lock_task("settings_post_save_task_lock")
def settings_post_save_task(settings: Settings, created: bool) -> None:

    print("--- settings_post_save_task ---")

    for product in Product.objects.filter(is_product_group=False):
        check_security_gate(product)

    print("--- after check_security_gate ---")

    if not created:
        if settings.feature_exploit_information and not Exploit_Information.objects.exists():

            print("--- settings.feature_exploit_information ---")

            import_cvss_bt()
        if not settings.feature_exploit_information and Exploit_Information.objects.exists():

            print("--- not settings.feature_exploit_information ---")

            Exploit_Information.objects.all().delete()
            apply_exploit_information_observations(settings)
