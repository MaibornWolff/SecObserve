import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django.http import HttpRequest

from application.access_control.models import User
from application.commons.services.log_message import format_log_message

logger = logging.getLogger("secobserve.access_control")


@receiver(user_logged_in)
def signal_user_logged_in(sender, request: HttpRequest, user: User, **kwargs) -> None:
    logger.info(format_log_message(message="User logged in", user=user))


@receiver(user_logged_out)
def signal_user_logged_out(sender, request: HttpRequest, user: User, **kwargs) -> None:
    logger.info(format_log_message(message="User logged out", user=user))


@receiver(user_login_failed)
def signal_user_login_failed(
    sender, request: HttpRequest, credentials: dict, **kwargs
) -> None:
    logger.info(format_log_message(message="User login failed: ", data=credentials))
