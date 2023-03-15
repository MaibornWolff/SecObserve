from django.dispatch import receiver
from constance.signals import config_updated

from application.core.queries.product import get_products
from application.core.services.security_gate import check_security_gate


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):

    if key.startswith("SECURITYGATE"):
        # ToDo: This can be called multiple times in parallel, when multiple fields get changed with 1 save.
        # Is this a problem?
        for product in get_products():
            check_security_gate(product)
