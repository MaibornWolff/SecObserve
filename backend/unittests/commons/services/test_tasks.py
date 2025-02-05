from unittest.mock import ANY, call, patch

from application.commons.services.tasks import handle_task_exception
from unittests.base_test_case import BaseTestCase


class TestTasks(BaseTestCase):
    @patch("inspect.currentframe")
    @patch("application.commons.services.tasks.send_task_exception_notification")
    @patch("application.commons.services.tasks.format_log_message")
    @patch("application.commons.services.tasks.logger.error")
    def test_handle_task_exception_without_frame(
        self,
        mock_logger,
        mock_format_log_message,
        mock_send_task_exception_notification,
        mock_currentframe,
    ):
        mock_currentframe.return_value = None
        exception = Exception("Test exception")
        handle_task_exception(exception, self.user_internal, self.product_1)

        self.assertEqual(mock_logger.call_count, 2)
        mock_format_log_message.assert_called_with(
            message="Error while executing background task",
            data={},
            exception=exception,
            user=self.user_internal,
        )
        mock_send_task_exception_notification.assert_called_with(
            function=None,
            arguments=None,
            user=self.user_internal,
            exception=exception,
            product=self.product_1,
        )
        mock_currentframe.assert_called_once()
