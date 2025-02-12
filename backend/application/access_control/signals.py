import logging
from typing import Any

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from application.access_control.models import (
    Authorization_Group,
    Authorization_Group_Member,
    User,
)
from application.commons.services.global_request import get_current_user
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.access_control")


@receiver(user_logged_in)
def signal_user_logged_in(  # pylint: disable=unused-argument
    sender: Any, user: User, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation
    logger.info(format_log_message(message="User logged in", user=user))


@receiver(user_logged_out)
def signal_user_logged_out(  # pylint: disable=unused-argument
    sender: Any, user: User, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation

    logger.info(format_log_message(message="User logged out", user=user))


@receiver(user_login_failed)
def signal_user_login_failed(  # pylint: disable=unused-argument
    sender: Any, credentials: dict, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation

    logger.info(format_log_message(message="User login failed: ", data=credentials))


@receiver(post_save, sender=Authorization_Group)
def authorization_group_post_save(  # pylint: disable=unused-argument
    sender: Any, instance: Authorization_Group, created: bool, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation
    _invalidate_oidc_groups_hashes()
    if created:
        user = get_current_user()
        if user and not user.is_superuser:
            Authorization_Group_Member.objects.create(
                authorization_group=instance, user=user, is_manager=True
            )


@receiver(post_delete, sender=Authorization_Group)
def authorization_group_post_delete(  # pylint: disable=unused-argument
    sender: Any, instance: Authorization_Group, **kwargs: Any
) -> None:
    # sender is needed according to Django documentation
    _invalidate_oidc_groups_hashes()


def _invalidate_oidc_groups_hashes() -> None:
    for user in User.objects.exclude(oidc_groups_hash=""):
        user.oidc_groups_hash = ""
        user.save()
