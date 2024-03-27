import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from application.access_control.models import Group, User
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.access_control")


@receiver(user_logged_in)
def signal_user_logged_in(  # pylint: disable=unused-argument
    sender, user: User, **kwargs
) -> None:
    # sender is needed according to Django documentation
    logger.info(format_log_message(message="User logged in", user=user))


@receiver(user_logged_out)
def signal_user_logged_out(  # pylint: disable=unused-argument
    sender, user: User, **kwargs
) -> None:
    # sender is needed according to Django documentation

    logger.info(format_log_message(message="User logged out", user=user))


@receiver(user_login_failed)
def signal_user_login_failed(  # pylint: disable=unused-argument
    sender, credentials: dict, **kwargs
) -> None:
    # sender is needed according to Django documentation

    logger.info(format_log_message(message="User login failed: ", data=credentials))


@receiver(post_save, sender=Group)
def branch_post_save(  # pylint: disable=unused-argument
    sender, instance: Group, created: bool, **kwargs
) -> None:
    # sender is needed according to Django documentation
    _invalidate_oidc_groups_hashes()


@receiver(post_delete, sender=Group)
def branch_post_delete(  # pylint: disable=unused-argument
    sender, instance: Group, **kwargs
) -> None:
    # sender is needed according to Django documentation
    _invalidate_oidc_groups_hashes()


def _invalidate_oidc_groups_hashes():
    for user in User.objects.exclude(oidc_groups_hash=""):
        user.oidc_groups_hash = ""
        user.save()
