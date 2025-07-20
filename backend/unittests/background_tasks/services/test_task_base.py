from unittest.mock import patch, MagicMock, call

from application.background_tasks.services.task_base import (
    handle_periodic_task_exception,
    so_periodic_task,
)
from unittests.base_test_case import BaseTestCase


class TestTaskBase(BaseTestCase):
    # ---------------------------------------------------------------
    # so_periodic_task
    # ---------------------------------------------------------------

    @patch("application.background_tasks.services.task_base.lock_task")
    @patch("application.background_tasks.services.task_base.logger")
    def test_so_periodic_task_successful_execution(self, mock_logger, mock_lock_task):
        # Setup
        mock_lock_task.return_value = lambda func: func
        test_function = MagicMock()
        test_function.__name__ = "test_function"
        
        # Execute
        decorated_function = so_periodic_task("test_task")(test_function)
        decorated_function()
        
        # Assert
        mock_logger.info.assert_has_calls([
            call("--- %s - start ---", "test_task"),
            call("--- %s - finished ---", "test_task")
        ])
        test_function.assert_called_once()
        mock_lock_task.assert_called_once_with("test_task")

    @patch("application.background_tasks.services.task_base.handle_periodic_task_exception")
    @patch("application.background_tasks.services.task_base.lock_task")
    @patch("application.background_tasks.services.task_base.logger")
    def test_so_periodic_task_exception_handling(self, mock_logger, mock_lock_task, mock_handle_exception):
        # Setup
        mock_lock_task.return_value = lambda func: func
        test_exception = Exception("Test exception")
        test_function = MagicMock(side_effect=test_exception)
        test_function.__name__ = "test_function"
        
        # Execute
        decorated_function = so_periodic_task("test_task")(test_function)
        decorated_function()
        
        # Assert
        mock_logger.info.assert_called_once_with("--- %s - start ---", "test_task")
        test_function.assert_called_once()
        mock_handle_exception.assert_called_once_with(test_exception)
        # Verify that the "finished" log is not called when an exception occurs
        self.assertEqual(mock_logger.info.call_count, 1)

    # ---------------------------------------------------------------
    # handle_periodic_task_exception
    # ---------------------------------------------------------------

    @patch("application.background_tasks.services.task_base.send_task_exception_notification")
    @patch("application.background_tasks.services.task_base.format_log_message")
    @patch("application.background_tasks.services.task_base.logger")
    @patch("application.background_tasks.services.task_base.sys.exc_info")
    @patch("application.background_tasks.services.task_base.inspect.getinnerframes")
    def test_handle_periodic_task_exception_with_function_name(
        self, mock_getinnerframes, mock_exc_info, mock_logger, mock_format_log_message, mock_send_notification
    ):
        # Setup
        test_exception = Exception("Test exception")
        mock_exc_info.return_value = (None, None, "traceback_object")
        
        # Create a mock frame with a function attribute
        mock_frame = MagicMock()
        mock_frame.function = "test_function"
        mock_getinnerframes.return_value = [MagicMock(), mock_frame]
        
        mock_format_log_message.return_value = "Formatted log message"
        
        # Execute
        handle_periodic_task_exception(test_exception)
        
        # Assert
        mock_exc_info.assert_has_calls([call(), call(), call(), call()])
        mock_getinnerframes.assert_called_once_with("traceback_object")
        
        # Check that format_log_message was called with the correct parameters
        mock_format_log_message.assert_called_once_with(
            message="Error while executing periodic background task",
            data={"function": "test_function"},
            exception=test_exception,
            username=None,
        )
        
        # Check that the error was logged
        mock_logger.error.assert_has_calls([
            call("Formatted log message"),
            call("NoneType: None\n")
        ])
        
        # Check that send_task_exception_notification was called with the correct parameters
        mock_send_notification.assert_called_once_with(
            function="test_function", arguments=None, user=None, exception=test_exception, product=None
        )

    @patch("application.background_tasks.services.task_base.send_task_exception_notification")
    @patch("application.background_tasks.services.task_base.format_log_message")
    @patch("application.background_tasks.services.task_base.logger")
    @patch("application.background_tasks.services.task_base.sys.exc_info")
    def test_handle_periodic_task_exception_without_frames(
        self, mock_exc_info, mock_logger, mock_format_log_message, mock_send_notification
    ):
        # Setup
        test_exception = Exception("Test exception")
        mock_exc_info.return_value = (None, None, None)
        mock_format_log_message.return_value = "Formatted log message"
        
        # Execute
        handle_periodic_task_exception(test_exception)
        
        # Assert
        mock_exc_info.assert_has_calls([call(), call(), call()])

        # Check that format_log_message was called with the correct parameters
        mock_format_log_message.assert_called_once_with(
            message="Error while executing periodic background task",
            data={},
            exception=test_exception,
            username=None,
        )
        
        # Check that the error was logged
        mock_logger.error.assert_has_calls([
            call("Formatted log message"),
            call("NoneType: None\n")
        ])
        
        # Check that send_task_exception_notification was called with the correct parameters
        mock_send_notification.assert_called_once_with(
            function=None, arguments=None, user=None, exception=test_exception, product=None
        )

    @patch("application.background_tasks.services.task_base.send_task_exception_notification")
    @patch("application.background_tasks.services.task_base.format_log_message")
    @patch("application.background_tasks.services.task_base.logger")
    @patch("application.background_tasks.services.task_base.sys.exc_info")
    @patch("application.background_tasks.services.task_base.inspect.getinnerframes")
    def test_handle_periodic_task_exception_with_insufficient_frames(
        self, mock_getinnerframes, mock_exc_info, mock_logger, mock_format_log_message, mock_send_notification
    ):
        # Setup
        test_exception = Exception("Test exception")
        mock_exc_info.return_value = (None, None, "traceback_object")
        
        # Create a mock frame with only one frame (less than required)
        mock_getinnerframes.return_value = [MagicMock()]
        
        mock_format_log_message.return_value = "Formatted log message"
        
        # Execute
        handle_periodic_task_exception(test_exception)
        
        # Assert
        mock_exc_info.assert_has_calls([call(), call(), call(), call()])
        mock_getinnerframes.assert_called_once_with("traceback_object")
        
        # Check that format_log_message was called with the correct parameters
        mock_format_log_message.assert_called_once_with(
            message="Error while executing periodic background task",
            data={},
            exception=test_exception,
            username=None,
        )
        
        # Check that the error was logged
        mock_logger.error.assert_has_calls([
            call("Formatted log message"),
            call("NoneType: None\n")
        ])
        
        # Check that send_task_exception_notification was called with the correct parameters
        mock_send_notification.assert_called_once_with(
            function=None, arguments=None, user=None, exception=test_exception, product=None
        )
