from typing import Any

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from application.access_control.services.roles_permissions import Roles
from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Product, Product_Member
from application.core.services.product import set_repository_default_branch
from application.core.services.security_gate import check_security_gate


@receiver(post_save, sender=Product)
def product_post_save(
    sender: Any,  # pylint: disable=unused-argument
    instance: Product,
    created: bool,
    **kwargs: Any,  # pylint: disable=unused-argument
) -> None:
    # sender is needed according to Django documentation
    if not created:
        if instance.is_product_group:
            for product in instance.products.all():
                check_security_gate(product)
        else:
            check_security_gate(instance)
    else:
        user = get_current_user()
        if user:
            Product_Member(product=instance, user=user, role=Roles.Owner).save()


@receiver(post_save, sender=Branch)
def branch_post_save(
    sender: Any,  # pylint: disable=unused-argument
    instance: Branch,
    created: bool,  # pylint: disable=unused-argument
    **kwargs: Any,  # pylint: disable=unused-argument
) -> None:
    # sender is needed according to Django documentation
    set_repository_default_branch(instance.product)


@receiver(post_delete, sender=Branch)
def branch_post_delete(sender: Any, instance: Branch, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    # sender is needed according to Django documentation
    set_repository_default_branch(instance.product)
