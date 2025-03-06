from typing import Any

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from application.access_control.services.roles_permissions import Roles
from application.commons.services.global_request import get_current_user
from application.core.models import Branch, Observation, Product, Product_Member
from application.core.services.observation import (
    get_identity_hash,
    normalize_observation_fields,
    set_product_flags,
)
from application.core.services.product import set_repository_default_branch
from application.core.services.security_gate import check_security_gate


@receiver(pre_save, sender=Observation)
def observation_pre_save(sender: Any, instance: Observation, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    # sender is needed according to Django documentation
    normalize_observation_fields(instance)
    instance.identity_hash = get_identity_hash(instance)
    set_product_flags(instance)


@receiver(post_save, sender=Product)
def product_post_save(
    sender: Any, instance: Product, created: bool, **kwargs: Any  # pylint: disable=unused-argument
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
    sender: Any, instance: Branch, created: bool, **kwargs: Any  # pylint: disable=unused-argument
) -> None:
    # sender is needed according to Django documentation
    set_repository_default_branch(instance.product)


@receiver(post_delete, sender=Branch)
def branch_post_delete(sender: Any, instance: Branch, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    # sender is needed according to Django documentation
    set_repository_default_branch(instance.product)
