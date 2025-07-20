from unittest.mock import MagicMock, patch

from application.background_tasks.periodic_tasks.license_tasks import (
    task_spdx_license_import,
)
from unittests.base_test_case import BaseTestCase


class TestLicenseTasks(BaseTestCase):
    # ---------------------------------------------------------------
    # task_spdx_license_import
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.license_tasks.import_licenses")
    @patch("application.background_tasks.periodic_tasks.license_tasks.Settings.load")
    def test_task_spdx_license_import_enabled(self, mock_settings_load, mock_import_licenses):
        # Setup
        mock_settings = MagicMock()
        mock_settings.feature_license_management = True
        mock_settings_load.return_value = mock_settings

        # Execute
        task_spdx_license_import()

        # Assert
        mock_settings_load.assert_called_once()
        mock_import_licenses.assert_called_once()

    @patch("application.background_tasks.periodic_tasks.license_tasks.import_licenses")
    @patch("application.background_tasks.periodic_tasks.license_tasks.Settings.load")
    def test_task_spdx_license_import_disabled(self, mock_settings_load, mock_import_licenses):
        # Setup
        mock_settings = MagicMock()
        mock_settings.feature_license_management = False
        mock_settings_load.return_value = mock_settings

        # Execute
        task_spdx_license_import()

        # Assert
        mock_settings_load.assert_called_once()
        mock_import_licenses.assert_not_called()
