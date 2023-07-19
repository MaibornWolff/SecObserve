from constance.signals import config_updated
from django.dispatch import receiver

from application.core.models import Product
from application.core.services.security_gate import check_security_gate


@receiver(config_updated)
def constance_updated(key, **kwargs):
    if key.startswith("SECURITY_GATE"):
        for product in Product.objects.filter(is_product_group=False):
            check_security_gate(product)
