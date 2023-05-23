import logging
import traceback
from datetime import datetime, timedelta
from typing import Optional

import requests
from constance import config
from django.core.mail import send_mail
from django.template.loader import render_to_string

from application.access_control.queries.user import get_user_by_email
from application.commons.services.functions import get_base_url_frontend, get_classname
from application.commons.services.log_message import format_log_message
from application.core.models import Product

logger = logging.getLogger("secobserve.commons")

LAST_EXCEPTIONS: dict[str, datetime] = {}


def send_product_security_gate_notification(product: Product) -> None:
    if product.security_gate_passed is None:
        security_gate_status = "None"
    elif product.security_gate_passed:
        security_gate_status = "Passed"
    else:
        security_gate_status = "Failed"

    email_to_adresses = _get_email_to_adresses(product.notification_email_to)
    if email_to_adresses and config.EMAIL_FROM:
        for notification_email_to in email_to_adresses:
            first_name = _get_first_name(notification_email_to)
            _send_email_notification(
                notification_email_to,
                f"Security gate for {product.name} has changed to {security_gate_status}",
                "email_product_security_gate.tpl",
                product=product,
                security_gate_status=security_gate_status,
                product_url=f"{get_base_url_frontend()}#/products/{product.id}/show",
                first_name=first_name,
            )

    if product.notification_ms_teams_webhook:
        _send_msteams_notification(
            product.notification_ms_teams_webhook,
            "msteams_product_security_gate.tpl",
            product=product,
            security_gate_status=security_gate_status,
            product_url=f"{get_base_url_frontend()}#/products/{product.id}/show",
        )


def send_exception_notification(exception: Exception) -> None:
    if _ratelimit_exception(exception):
        email_to_adresses = _get_email_to_adresses(config.EXCEPTION_EMAIL_TO)
        if email_to_adresses and config.EMAIL_FROM:
            for notification_email_to in email_to_adresses:
                first_name = _get_first_name(notification_email_to)
                _send_email_notification(
                    notification_email_to,
                    f"Exception {get_classname(exception)} has occured",
                    "email_exception.tpl",
                    exception_class=get_classname(exception),
                    exception_message=str(exception),
                    exception_trace=_get_stack_trace(exception, False),
                    date_time=datetime.now(),
                    first_name=first_name,
                )

        if config.EXCEPTION_MS_TEAMS_WEBHOOK:
            _send_msteams_notification(
                config.EXCEPTION_MS_TEAMS_WEBHOOK,
                "msteams_exception.tpl",
                exception_class=get_classname(exception),
                exception_message=str(exception),
                exception_trace=_get_stack_trace(exception, True),
                date_time=datetime.now(),
            )


def _send_email_notification(
    notification_email_to: str, subject: str, template: str, **kwargs
) -> None:
    notification_message = _create_notification_message(template, **kwargs)
    if notification_message:
        try:
            send_mail(
                subject=subject,
                message=notification_message,
                from_email=config.EMAIL_FROM,
                recipient_list=[notification_email_to],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(
                format_log_message(
                    message=f"Error while sending email to {notification_email_to}",
                    exception=e,
                )
            )


def _send_msteams_notification(webhook: str, template: str, **kwargs) -> None:
    notification_message = _create_notification_message(template, **kwargs)
    if notification_message:
        try:
            response = requests.request(
                method="POST",
                url=webhook,
                data=notification_message,
                timeout=60,
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(
                format_log_message(
                    message=f"Error while calling MS Teams webhook {webhook}",
                    exception=e,
                )
            )


def _create_notification_message(template: str, **kwargs) -> Optional[str]:
    try:
        return render_to_string(template, kwargs)
    except Exception as e:
        logger.error(
            format_log_message(
                message=f"Error while rendering template {template}",
                exception=e,
            )
        )
        return None


def _ratelimit_exception(exception: Exception) -> bool:
    key = get_classname(exception) + "/" + str(exception)
    now = datetime.now()
    if key in LAST_EXCEPTIONS:
        last_datetime = LAST_EXCEPTIONS[key]
        difference: timedelta = now - last_datetime
        if difference.seconds >= config.EXCEPTION_RATELIMIT:
            LAST_EXCEPTIONS[key] = now
            return True

        return False

    LAST_EXCEPTIONS[key] = now
    return True


def _get_email_to_adresses(notification_email_to: str) -> list[str]:
    email_to_adresses = notification_email_to.split(",")
    return [item.strip() for item in email_to_adresses]


def _get_first_name(email: str) -> str:
    user = get_user_by_email(email)
    if user and user.first_name:
        return f" {user.first_name}"
    return ""


def _get_stack_trace(exc: Exception, msteams: bool) -> str:
    if msteams:
        delimiter = "/n/n"
    else:
        delimiter = ""
    return delimiter.join(traceback.format_tb(exc.__traceback__))
