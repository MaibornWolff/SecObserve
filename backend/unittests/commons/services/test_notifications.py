from datetime import datetime, timedelta
from unittest.mock import ANY, patch

from constance.test import override_config
from requests import Response

from application.commons.services.functions import get_classname
from application.commons.services.notifications import (
    LAST_EXCEPTIONS,
    _create_notification_message,
    _get_base_url_frontend,
    _ratelimit_exception,
    _send_notification,
    send_exception_notification,
    send_product_security_gate_notification,
)
from unittests.base_test_case import BaseTestCase


class TestNotifications(BaseTestCase):
    # --- send_product_security_gate_notification ---

    @patch("application.commons.services.notifications._send_notification")
    def test_send_product_security_gate_notification_no_webhook(self, mock_send):
        self.product_1.ms_teams_webhook = ""
        send_product_security_gate_notification(self.product_1)
        mock_send.assert_not_called()

    @patch("application.commons.services.notifications._send_notification")
    @patch("application.commons.services.notifications._get_base_url_frontend")
    def test_send_product_security_gate_notification_security_gate_none(
        self, mock_base_url, mock_send
    ):
        mock_base_url.return_value = "https://secobserve.com/"
        self.product_1.ms_teams_webhook = "https://msteams.microsoft.com"
        self.product_1.security_gate_passed = None
        send_product_security_gate_notification(self.product_1)
        mock_send.assert_called_with(
            "https://msteams.microsoft.com",
            "msteams_product_security_gate.tpl",
            product=self.product_1,
            security_gate_status="None",
            product_url="https://secobserve.com/#/products/None/show",
        )

    @patch("application.commons.services.notifications._send_notification")
    @patch("application.commons.services.notifications._get_base_url_frontend")
    def test_send_product_security_gate_notification_security_gate_passed(
        self, mock_base_url, mock_send
    ):
        mock_base_url.return_value = "https://secobserve.com/"
        self.product_1.ms_teams_webhook = "https://msteams.microsoft.com"
        self.product_1.security_gate_passed = True
        send_product_security_gate_notification(self.product_1)
        mock_send.assert_called_with(
            "https://msteams.microsoft.com",
            "msteams_product_security_gate.tpl",
            product=self.product_1,
            security_gate_status="Passed",
            product_url="https://secobserve.com/#/products/None/show",
        )

    @patch("application.commons.services.notifications._send_notification")
    @patch("application.commons.services.notifications._get_base_url_frontend")
    def test_send_product_security_gate_notification_security_gate_failed(
        self, mock_base_url, mock_send
    ):
        mock_base_url.return_value = "https://secobserve.com/"
        self.product_1.ms_teams_webhook = "https://msteams.microsoft.com"
        self.product_1.security_gate_passed = False
        send_product_security_gate_notification(self.product_1)
        mock_send.assert_called_with(
            "https://msteams.microsoft.com",
            "msteams_product_security_gate.tpl",
            product=self.product_1,
            security_gate_status="Failed",
            product_url="https://secobserve.com/#/products/None/show",
        )

    # --- send_exception_notification ---

    @override_config(EXCEPTION_MS_TEAMS_WEBHOOK="")
    @patch("application.commons.services.notifications._ratelimit_exception")
    @patch("application.commons.services.notifications._send_notification")
    def test_send_exception_notification_no_webhook(self, mock_send, mock_ratelimit):
        mock_ratelimit.return_value = True
        send_exception_notification(Exception("test_exception"))
        mock_send.assert_not_called()

    @override_config(EXCEPTION_MS_TEAMS_WEBHOOK="https://msteams.microsoft.com")
    @patch("application.commons.services.notifications._ratelimit_exception")
    @patch("application.commons.services.notifications._send_notification")
    def test_send_exception_notification_no_ratelimit(self, mock_send, mock_ratelimit):
        mock_ratelimit.return_value = False
        exception = Exception("test_exception")
        send_exception_notification(exception)
        mock_ratelimit.assert_called_with(exception)
        mock_send.assert_not_called()

    @override_config(EXCEPTION_MS_TEAMS_WEBHOOK="https://msteams.microsoft.com")
    @patch("application.commons.services.notifications._ratelimit_exception")
    @patch("application.commons.services.notifications._send_notification")
    def test_send_exception_notification_success(self, mock_send, mock_ratelimit):
        mock_ratelimit.return_value = True
        exception = Exception("test_exception")
        send_exception_notification(exception)
        mock_ratelimit.assert_called_with(exception)
        mock_send.assert_called_with(
            "https://msteams.microsoft.com",
            "msteams_exception.tpl",
            exception_class="builtins.Exception",
            exception_message="test_exception",
            date_time=ANY,
        )

    # --- _send_notification ---

    @patch("application.commons.services.notifications._create_notification_message")
    @patch("application.commons.services.notifications.requests.request")
    def test_send_notification_empty_message(self, mock_request, mock_create_message):
        mock_create_message.return_value = None

        _send_notification("test_webhook", "test_template")

        mock_create_message.assert_called_with("test_template")
        mock_request.assert_not_called()

    @patch("application.commons.services.notifications._create_notification_message")
    @patch("application.commons.services.notifications.requests.request")
    @patch("application.commons.services.notifications.logger.error")
    @patch("application.commons.services.notifications.format_log_message")
    def test_send_notification_exception(
        self, mock_format, mock_logger, mock_request, mock_create_message
    ):
        mock_create_message.return_value = "test_message"
        mock_request.side_effect = Exception("test_exception")

        _send_notification("test_webhook", "test_template")

        mock_create_message.assert_called_with("test_template")
        mock_request.assert_called_with(
            method="POST", url="test_webhook", data="test_message", timeout=60
        )
        mock_logger.assert_called_once()
        mock_format.assert_called_once()

    @patch("application.commons.services.notifications._create_notification_message")
    @patch("application.commons.services.notifications.requests.request")
    @patch("application.commons.services.notifications.logger.error")
    @patch("application.commons.services.notifications.format_log_message")
    def test_send_notification_not_ok(
        self, mock_format, mock_logger, mock_request, mock_create_message
    ):
        mock_create_message.return_value = "test_message"
        response = Response()
        response.status_code = 400
        mock_request.return_value = response

        _send_notification("test_webhook", "test_template")

        mock_create_message.assert_called_with("test_template")
        mock_request.assert_called_with(
            method="POST", url="test_webhook", data="test_message", timeout=60
        )
        mock_logger.assert_called_once()
        mock_format.assert_called_once()

    @patch("application.commons.services.notifications._create_notification_message")
    @patch("application.commons.services.notifications.requests.request")
    @patch("application.commons.services.notifications.logger.error")
    @patch("application.commons.services.notifications.format_log_message")
    def test_send_notification_success(
        self, mock_format, mock_logger, mock_request, mock_create_message
    ):
        mock_create_message.return_value = "test_message"
        response = Response()
        response.status_code = 200
        mock_request.return_value = response

        _send_notification("test_webhook", "test_template")

        mock_create_message.assert_called_with("test_template")
        mock_request.assert_called_with(
            method="POST", url="test_webhook", data="test_message", timeout=60
        )
        mock_logger.assert_not_called()
        mock_format.assert_not_called()

    # --- _create_notification_message ---

    @patch("application.commons.services.notifications.logger.error")
    @patch("application.commons.services.notifications.format_log_message")
    def test_create_notification_message_not_found(self, mock_format, mock_logging):
        message = _create_notification_message("invalid_template_name.tpl")
        self.assertIsNone(message)
        mock_logging.assert_called_once()
        mock_format.assert_called_once()

    def test_create_notification_message_security_gate(self):
        message = _create_notification_message(
            "msteams_product_security_gate.tpl",
            product=self.product_1,
            security_gate_status="security_gate_passed",
            product_url="product_url",
        )

        expected_message = """{
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "title": "Security gate for product product_1 has changed to security_gate_passed",
    "summary": "Security gate for product product_1 has changed to security_gate_passed",
    "potentialAction": [
        {
            "@type": "OpenUri",
            "name": "View Product product_1",
            "targets": [
                {
                    "os": "default",
                    "uri": "product_url"
                }
            ]
        }
    ]
}
"""
        self.assertEqual(expected_message, message)

    def test_create_notification_message_exception(self):
        exception = Exception("test_exception")
        message = _create_notification_message(
            "msteams_exception.tpl",
            exception_class=get_classname(exception),
            exception_message=str(exception),
            date_time=datetime(2022, 12, 31, 23, 59, 59),
        )

        expected_message = """{
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "title": "Exception builtins.Exception has occured",
    "summary": "Exception builtins.Exception has occured",
    "sections": [{
        "facts": [{
            "name": "Exception class:",
            "value": "builtins.Exception"
        }, {
            "name": "Exception message:",
            "value": "test_exception"
        }, {
            "name": "Date:",
            "value": "2022-12-31 23:59:59.000000"
        }],
        "markdown": true
    }],
}
"""
        self.assertEqual(expected_message, message)

    # --- _get_base_url_frontend ---

    @override_config(BASE_URL_FRONTEND="https://www.example.com")
    def test_get_base_url_frontend_without_slash(self):
        self.assertEqual("https://www.example.com/", _get_base_url_frontend())

    @override_config(BASE_URL_FRONTEND="https://www.example.com/")
    def test_get_base_url_frontend_with_slash(self):
        self.assertEqual("https://www.example.com/", _get_base_url_frontend())

    # --- _ratelimit_exception ---

    def test_ratelimit_exception_new_key(self):
        LAST_EXCEPTIONS.clear()
        exception = Exception("test_exception")

        self.assertTrue(_ratelimit_exception(exception))
        self.assertEqual(1, len(LAST_EXCEPTIONS.keys()))
        difference: timedelta = (
            datetime.now() - LAST_EXCEPTIONS["builtins.Exception/test_exception"]
        )
        self.assertGreater(difference.microseconds, 0)
        self.assertLess(difference.microseconds, 999)

    @override_config(EXCEPTION_RATELIMIT=10)
    def test_ratelimit_exception_true(self):
        LAST_EXCEPTIONS.clear()
        LAST_EXCEPTIONS[
            "builtins.Exception/test_exception"
        ] = datetime.now() - timedelta(seconds=11)
        exception = Exception("test_exception")

        self.assertTrue(_ratelimit_exception(exception))
        self.assertEqual(1, len(LAST_EXCEPTIONS.keys()))

    @override_config(EXCEPTION_RATELIMIT=10)
    def test_ratelimit_exception_false(self):
        LAST_EXCEPTIONS.clear()
        LAST_EXCEPTIONS[
            "builtins.Exception/test_exception"
        ] = datetime.now() - timedelta(seconds=9)
        exception = Exception("test_exception")

        self.assertFalse(_ratelimit_exception(exception))
        self.assertEqual(1, len(LAST_EXCEPTIONS.keys()))
