import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from application.access_control.models import User
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.access_control")


@receiver(user_logged_in)
def signal_user_logged_in(sender, user: User, **kwargs) -> None:
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
