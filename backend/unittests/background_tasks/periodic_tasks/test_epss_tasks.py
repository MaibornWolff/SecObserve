from unittest.mock import patch

from application.background_tasks.periodic_tasks.epss_tasks import task_import_epss
from unittests.base_test_case import BaseTestCase


class TestEpssTasks(BaseTestCase):
    # ---------------------------------------------------------------
    # task_import_epss
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.epss_tasks.import_cvss_bt")
    @patch("application.background_tasks.periodic_tasks.epss_tasks.epss_apply_observations")
    @patch("application.background_tasks.periodic_tasks.epss_tasks.import_epss")
    def test_task_import_epss(self, mock_import_epss, mock_epss_apply_observations, mock_import_cvss_bt):
        # Execute
        task_import_epss()

        # Assert
        mock_import_epss.assert_called_once()
        mock_epss_apply_observations.assert_called_once()
        mock_import_cvss_bt.assert_called_once()

    @patch("application.background_tasks.periodic_tasks.epss_tasks.import_cvss_bt")
    @patch("application.background_tasks.periodic_tasks.epss_tasks.epss_apply_observations")
    @patch("application.background_tasks.periodic_tasks.epss_tasks.import_epss")
    def test_task_import_epss_execution_order(
        self, mock_import_epss, mock_epss_apply_observations, mock_import_cvss_bt
    ):
        # Execute
        task_import_epss()

        # Assert - Check execution order
        self.assertEqual(mock_import_epss.call_count, 1)
        self.assertEqual(mock_epss_apply_observations.call_count, 1)
        self.assertEqual(mock_import_cvss_bt.call_count, 1)

        # Verify the order of execution
        mock_import_epss.assert_called_once()
        mock_epss_apply_observations.assert_called_once()
        mock_import_cvss_bt.assert_called_once()
