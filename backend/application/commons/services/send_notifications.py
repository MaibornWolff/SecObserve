import logging
import traceback
from datetime import datetime, timedelta
from typing import Optional

import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string

from application.access_control.models import User
from application.access_control.queries.user import get_user_by_email
from application.commons.models import Notification, Settings
from application.commons.services.functions import get_base_url_frontend, get_classname
from application.commons.services.global_request import get_current_user
from application.commons.services.log_message import format_log_message
from application.core.models import Product

logger = logging.getLogger("secobserve.commons")

LAST_EXCEPTIONS: dict[str, datetime] = {}


def send_product_security_gate_notification(product: Product) -> None:
    settings = Settings.load()

    if product.security_gate_passed is None:
        security_gate_status = "None"
    elif product.security_gate_passed:
        security_gate_status = "Passed"
    else:
        security_gate_status = "Failed"

    notification_email_to = _get_notification_email_to(product)
    email_to_addresses = _get_email_to_addresses(notification_email_to)
    if email_to_addresses and settings.email_from:
        for email_to_address in email_to_addresses:
            first_name = _get_first_name(email_to_address)
            _send_email_notification(
                email_to_address,
                f"Security gate for {product.name} has changed to {security_gate_status}",
                "email_product_security_gate.tpl",
                product=product,
                security_gate_status=security_gate_status,
                product_url=f"{get_base_url_frontend()}#/products/{product.id}/show",
                first_name=first_name,
            )

    notification_ms_teams_webhook = _get_notification_ms_teams_webhook(product)
    if notification_ms_teams_webhook:
        _send_msteams_notification(
            notification_ms_teams_webhook,
            "msteams_product_security_gate.tpl",
            product=product,
            security_gate_status=security_gate_status,
            product_url=f"{get_base_url_frontend()}#/products/{product.id}/show",
        )

    notification_slack_webhook = _get_notification_slack_webhook(product)
    if notification_slack_webhook:
        _send_slack_notification(
            notification_slack_webhook,
            "slack_product_security_gate.tpl",
            product=product,
            security_gate_status=security_gate_status,
            product_url=f"{get_base_url_frontend()}#/products/{product.id}/show",
        )

    Notification.objects.create(
        name=f"Security gate has changed to {security_gate_status}",
        product=product,
        user=get_current_user(),
        type=Notification.TYPE_SECURITY_GATE,
    )


def send_exception_notification(exception: Exception) -> None:
    settings = Settings.load()

    if _ratelimit_exception(exception):
        email_to_adresses = _get_email_to_addresses(settings.exception_email_to)
        if email_to_adresses and settings.email_from:
            for notification_email_to in email_to_adresses:
                first_name = _get_first_name(notification_email_to)
                _send_email_notification(
                    notification_email_to,
                    f'Exception "{get_classname(exception)}" has occured',
                    "email_exception.tpl",
                    exception_class=get_classname(exception),
                    exception_message=str(exception),
                    exception_trace=_get_stack_trace(exception, False),
                    date_time=datetime.now(),
                    first_name=first_name,
                )

        if settings.exception_ms_teams_webhook:
            _send_msteams_notification(
                settings.exception_ms_teams_webhook,
                "msteams_exception.tpl",
                exception_class=get_classname(exception),
                exception_message=str(exception),
                exception_trace=_get_stack_trace(exception, True),
                date_time=datetime.now(),
            )

        if settings.exception_slack_webhook:
            _send_slack_notification(
                settings.exception_slack_webhook,
                "slack_exception.tpl",
                exception_class=get_classname(exception),
                exception_message=str(exception),
                exception_trace=_get_stack_trace(exception, True),
                date_time=datetime.now(),
            )

        Notification.objects.create(
            name=f'Exception "{get_classname(exception)}" has occured',
            message=str(exception),
            user=get_current_user(),
            type=Notification.TYPE_EXCEPTION,
        )


def send_task_exception_notification(
    function: Optional[str],
    arguments: Optional[dict],
    user: Optional[User],
    exception: Exception,
) -> None:
    settings = Settings.load()

    if _ratelimit_exception(exception, function, arguments):
        email_to_adresses = _get_email_to_addresses(settings.exception_email_to)
        if email_to_adresses and settings.email_from:
            for notification_email_to in email_to_adresses:
                first_name = _get_first_name(notification_email_to)
                _send_email_notification(
                    notification_email_to,
                    f'Exception "{get_classname(exception)}" has occured in background task',
                    "email_task_exception.tpl",
                    function=function,
                    arguments=str(arguments),
                    user=user,
                    exception_class=get_classname(exception),
                    exception_message=str(exception),
                    exception_trace=_get_stack_trace(exception, False),
                    date_time=datetime.now(),
                    first_name=first_name,
                )

        if settings.exception_ms_teams_webhook:
            _send_msteams_notification(
                settings.exception_ms_teams_webhook,
                "msteams_task_exception.tpl",
                function=function,
                arguments=str(arguments),
                user=user,
                exception_class=get_classname(exception),
                exception_message=str(exception),
                exception_trace=_get_stack_trace(exception, True),
                date_time=datetime.now(),
            )

        if settings.exception_slack_webhook:
            _send_slack_notification(
                settings.exception_slack_webhook,
                "slack_task_exception.tpl",
                function=function,
                arguments=str(arguments),
                user=user,
                exception_class=get_classname(exception),
                exception_message=str(exception),
                exception_trace=_get_stack_trace(exception, True),
                date_time=datetime.now(),
            )

        product = None
        observation = None
        if arguments:
            observation = arguments.get("observation")
            if observation:
                product = observation.product

        Notification.objects.create(
            name=f'Exception "{get_classname(exception)}" has occured',
            message=str(exception),
            function=str(function),
            arguments=_get_arguments_string(arguments),
            product=product,
            observation=observation,
            user=user,
            type=Notification.TYPE_TASK,
        )


def _send_email_notification(
    notification_email_to: str, subject: str, template: str, **kwargs
) -> None:
    settings = Settings.load()

    notification_message = _create_notification_message(template, **kwargs)
    if notification_message:
        try:
            send_mail(
                subject=subject,
                message=notification_message,
                from_email=settings.email_from,
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
        notification_message = notification_message.replace("&quot;", '\\"')
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


def _send_slack_notification(webhook: str, template: str, **kwargs) -> None:
    notification_message = _create_notification_message(template, **kwargs)
    if notification_message:
        notification_message = notification_message.replace("&#x27;", "\\'")
        notification_message = notification_message.replace("&quot;", '\\"')
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
                    message=f"Error while calling Slack webhook {webhook}",
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


def _ratelimit_exception(
    exception: Exception, function: str = None, arguments: dict = None
) -> bool:
    settings = Settings.load()

    key = (
        get_classname(exception)
        + "/"
        + str(exception)
        + "/"
        + str(function)
        + "/"
        + _get_arguments_string(arguments)
    )
    now = datetime.now()

    if key in LAST_EXCEPTIONS:
        last_datetime = LAST_EXCEPTIONS[key]
        difference: timedelta = now - last_datetime
        if difference.seconds >= settings.exception_rate_limit:
            LAST_EXCEPTIONS[key] = now
            return True

        return False

    LAST_EXCEPTIONS[key] = now
    return True


def _get_notification_email_to(product: Product) -> Optional[str]:
    if product.notification_email_to:
        return product.notification_email_to

    if product.product_group and product.product_group.notification_email_to:
        return product.product_group.notification_email_to

    return None


def _get_notification_ms_teams_webhook(product: Product) -> Optional[str]:
    if product.notification_ms_teams_webhook:
        return product.notification_ms_teams_webhook

    if product.product_group and product.product_group.notification_ms_teams_webhook:
        return product.product_group.notification_ms_teams_webhook

    return None


def _get_notification_slack_webhook(product: Product) -> Optional[str]:
    if product.notification_slack_webhook:
        return product.notification_slack_webhook

    if product.product_group and product.product_group.notification_slack_webhook:
        return product.product_group.notification_slack_webhook

    return None


def _get_email_to_addresses(
    notification_email_to: Optional[str],
) -> Optional[list[str]]:
    if not notification_email_to:
        return None

    email_to_adresses = notification_email_to.split(",")
    return [item.strip() for item in email_to_adresses]


def _get_first_name(email: str) -> str:
    user = get_user_by_email(email)
    if user and user.first_name:
        return f" {user.first_name}"
    return ""


def _get_stack_trace(exc: Exception, format_as_code: bool) -> str:
    delimiter = ""
    stack_trace = delimiter.join(traceback.format_tb(exc.__traceback__))

    if stack_trace and format_as_code:
        stack_trace = f"```\n{stack_trace}\n```"

    return stack_trace


def _get_arguments_string(arguments: Optional[dict]) -> str:
    if arguments:
        return str(arguments)
    return ""
