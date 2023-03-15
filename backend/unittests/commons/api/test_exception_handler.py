from unittest.mock import patch
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
    APIException,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from unittests.base_test_case import BaseTestCase
from application.commons.api.exception_handler import custom_exception_handler


class TestExceptionHandler(BaseTestCase):
    def test_protected_error(self):
        exception = ProtectedError(
            "Cannot delete some instances of model 'Product' because they are referenced through protected foreign keys: 'Observation.product'.",
            None,
        )
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_409_CONFLICT, response.status_code)
        data = {
            "message": "Cannot delete some instances of model 'Product' because they are referenced through protected foreign keys"
        }
        self.assertEqual(data, response.data)

    @patch("application.commons.api.exception_handler.logger.error")
    @patch("application.commons.api.exception_handler.format_log_message")
    @patch("application.commons.api.exception_handler.send_exception_notification")
    def test_no_response(self, mock_notify, mock_format, mock_logging):
        exception = Exception("Something unexpected has happened")
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        data = {"message": "Internal server error, check logs for details"}
        self.assertEqual(data, response.data)
        mock_notify.assert_called_with(exception)
        mock_format.assert_called_with(response=response, exception=exception)
        self.assertEqual(mock_logging.call_count, 2)

    @patch("application.commons.api.exception_handler.logger.warning")
    @patch("application.commons.api.exception_handler.format_log_message")
    def test_authentication_failed(self, mock_format, mock_logging):
        exception = AuthenticationFailed("Authentication has failed")
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)
        data = {"message": "Authentication has failed"}
        self.assertEqual(data, response.data)
        mock_format.assert_called_with(response=response, exception=exception)
        mock_logging.assert_called_once()

    @patch("application.commons.api.exception_handler.logger.warning")
    @patch("application.commons.api.exception_handler.format_log_message")
    def test_permission_denied(self, mock_format, mock_logging):
        exception = PermissionDenied("Not authentication")
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code)
        data = {"message": "Not authentication"}
        self.assertEqual(data, response.data)
        mock_format.assert_called_with(response=response, exception=exception)
        mock_logging.assert_called_once()

    @patch("application.commons.api.exception_handler.logger.warning")
    @patch("application.commons.api.exception_handler.format_log_message")
    def test_other_user_error(self, mock_format, mock_logging):
        exception = ValidationError("Not validated")
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        data = {"message": "Not validated"}
        self.assertEqual(data, response.data)
        mock_format.assert_not_called()
        mock_logging.assert_not_called()

    @patch("application.commons.api.exception_handler.logger.error")
    @patch("application.commons.api.exception_handler.format_log_message")
    def test_server_error(self, mock_format, mock_logging):
        exception = APIException(Exception("Not authentication"))
        response = custom_exception_handler(exception, None)

        self.assertEqual(HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        data = {"message": "Internal server error, check logs for details"}
        self.assertEqual(data, response.data)
        mock_format.assert_called_with(response=response, exception=exception)
        self.assertEqual(mock_logging.call_count, 2)
