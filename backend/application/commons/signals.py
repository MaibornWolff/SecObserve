from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from application.commons.models import Settings
from application.core.models import Product
from application.core.services.security_gate import check_security_gate


@receiver(post_save, sender=Settings)
def settings_post_save(  # pylint: disable=unused-argument
    sender: Any, instance: Settings, created: bool, **kwargs: Any
) -> None:
    # parameters are needed according to Django documentation
    for product in Product.objects.filter(is_product_group=False):
        check_security_gate(product)
