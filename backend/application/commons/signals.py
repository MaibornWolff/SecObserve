from typing import Any

import environ
from django.db.models.signals import post_save
from django.dispatch import receiver
from huey.contrib.djhuey import db_task, lock_task

from application.commons.models import Settings
from application.core.models import Product
from application.core.services.security_gate import check_security_gate
from application.epss.models import Enriched_CVSS
from application.epss.services.cvss_bt import (
    enriched_cvss_apply_observations,
    import_cvss_bt,
)


@receiver(post_save, sender=Settings)
def settings_post_save(  # pylint: disable=unused-argument
    sender: Any, instance: Settings, created: bool, **kwargs: Any
) -> None:
    # parameters are needed according to Django documentation
    env = environ.Env()
    if not env.bool("SO_UNITTESTS", False):
        settings_post_save_task(instance)


@db_task()
@lock_task("settings_post_save_task_lock")
def settings_post_save_task(settings: Settings) -> None:
    for product in Product.objects.filter(is_product_group=False):
        check_security_gate(product)

    if settings.feature_cvss_enrichment and not Enriched_CVSS.objects.exists():
        import_cvss_bt()

    if not settings.feature_cvss_enrichment and Enriched_CVSS.objects.exists():
        Enriched_CVSS.objects.all().delete()
        enriched_cvss_apply_observations(settings)
