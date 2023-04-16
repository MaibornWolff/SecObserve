from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.db.models.deletion import ProtectedError
from django.http.request import HttpRequest
from rest_framework.response import Response

from application.commons.services.log_message import format_log_message
from unittests.base_test_case import BaseTestCase


class TestLogMessage(BaseTestCase):
    @patch("application.commons.services.log_message.get_current_user")
    @patch("application.commons.services.log_message.get_current_request")
    def test_format_log_message_empty(self, mock_request, mock_user):
        mock_request.return_value = None
        mock_user.return_value = None

        message = format_log_message()

        self.assertEqual("{'message': 'No message given'}", message)

    @patch("application.commons.services.log_message.get_current_user")
    @patch("application.commons.services.log_message.get_current_request")
    def test_format_log_message_full(self, mock_request, mock_user):
        mock_request.return_value = None
        mock_user.return_value = None

        message = format_log_message(
            message="incoming_message",
            data={"key_1": "value_1", "key_2": "value_2"},
            user=self.user_internal,
            response=Response(status=500),
            exception=Exception("exception_message"),
        )

        log_message = "{'message': 'incoming_message', 'data_key_1': 'value_1', 'data_key_2': 'value_2', 'user': 'user_internal@example.com', 'response_status': '500', 'exception_message': 'exception_message', 'exception_class': 'builtins.Exception'}"
        self.assertEqual(log_message, message)

    @patch("application.commons.services.log_message.get_current_user")
    @patch("application.commons.services.log_message.get_current_request")
    def test_format_log_message_anonymous_user(self, mock_request, mock_user):
        mock_request.return_value = None
        mock_user.return_value = AnonymousUser()

        message = format_log_message(message="test_message")

        log_message = "{'message': 'test_message'}"
        self.assertEqual(log_message, message)

    @patch("application.commons.services.log_message.get_current_user")
    @patch("application.commons.services.log_message.get_current_request")
    def test_format_log_message_medium_1(self, mock_request, mock_user):
        request = HttpRequest()
        request.META["HTTP_X_FORWARDED_FOR"] = "addr_0, addr_1"
        request.method = "POST"
        mock_request.return_value = request
        mock_user.return_value = self.user_external

        message = format_log_message(exception=ProtectedError("protected_error", None))

        log_message = "{'message': \"('protected_error', None)\", 'user': 'user_external@example.com', 'request_method': 'POST', 'request_path': '', 'request_client_ip': 'addr_0', 'exception_class': 'django.db.models.deletion.ProtectedError'}"
        self.assertEqual(log_message, message)

    @patch("application.commons.services.log_message.get_current_user")
    @patch("application.commons.services.log_message.get_current_request")
    def test_format_log_message_medium_2(self, mock_request, mock_user):
        request = HttpRequest()
        request.path = "request_path"
        request.method = "GET"
        request.META["REMOTE_ADDR"] = "addr"
        mock_request.return_value = request
        mock_user.return_value = self.user_external

        message = format_log_message(exception=ProtectedError("protected_error", None))

        log_message = "{'message': \"('protected_error', None)\", 'user': 'user_external@example.com', 'request_method': 'GET', 'request_path': 'request_path', 'request_client_ip': 'addr', 'exception_class': 'django.db.models.deletion.ProtectedError'}"
        self.assertEqual(log_message, message)
