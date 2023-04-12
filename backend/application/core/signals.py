from django.db.models.signals import post_save
from django.dispatch import receiver

from application.access_control.services.roles_permissions import Roles
from application.commons.services.global_request import get_current_user
from application.core.models import Product, Product_Member
from application.core.services.security_gate import check_security_gate


@receiver(post_save, sender=Product)
def product_post_save(  # pylint: disable=unused-argument
    sender, instance: Product, created: bool, **kwargs
) -> None:
    # sender is needed according to Django documentation
    if not created:
        check_security_gate(instance)
    else:
        user = get_current_user()
        if user:
            Product_Member(product=instance, user=user, role=Roles.Owner).save()
