from unittest.mock import MagicMock, call, patch

from application.background_tasks.periodic_tasks.import_observations_tasks import (
    task_api_import,
)
from unittests.base_test_case import BaseTestCase


class TestImportObservationsTasks(BaseTestCase):
    # ---------------------------------------------------------------
    # task_api_import
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.scan_product")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.api_import_observations")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Product.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Api_Configuration.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Settings.load")
    def test_task_api_import_all_enabled(
        self,
        mock_settings_load,
        mock_api_config_filter,
        mock_product_filter,
        mock_api_import_observations,
        mock_scan_product,
    ):
        # Setup
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.feature_automatic_api_import = True
        mock_settings.feature_automatic_osv_scanning = True
        mock_settings_load.return_value = mock_settings

        # Mock API configurations
        mock_api_config = MagicMock()
        mock_api_config.automatic_import_branch = "main"
        mock_api_config.automatic_import_service = "service1"
        mock_api_config.automatic_import_docker_image_name_tag = "image:tag"
        mock_api_config.automatic_import_endpoint_url = "https://example.com"
        mock_api_config.automatic_import_kubernetes_cluster = "cluster1"
        mock_api_config_filter.return_value = [mock_api_config]

        # Mock products
        mock_product = MagicMock()
        mock_product_filter.return_value = [mock_product]

        # Mock import results
        mock_api_import_observations.return_value = (1, 2, 3)  # new, updated, resolved
        mock_scan_product.return_value = (4, 5, 6)  # new, updated, resolved

        # Execute
        task_api_import()

        # Assert
        # Check settings were loaded twice (once for API import, once for OSV)
        self.assertEqual(mock_settings_load.call_count, 2)

        # Check API import was called with correct parameters
        mock_api_config_filter.assert_called_once_with(automatic_import_enabled=True)
        mock_api_import_observations.assert_called_once()
        api_import_params = mock_api_import_observations.call_args[0][0]
        self.assertEqual(api_import_params.api_configuration, mock_api_config)
        self.assertEqual(api_import_params.branch, mock_api_config.automatic_import_branch)
        self.assertEqual(api_import_params.service, mock_api_config.automatic_import_service)
        self.assertEqual(
            api_import_params.docker_image_name_tag, mock_api_config.automatic_import_docker_image_name_tag
        )
        self.assertEqual(api_import_params.endpoint_url, mock_api_config.automatic_import_endpoint_url)
        self.assertEqual(api_import_params.kubernetes_cluster, mock_api_config.automatic_import_kubernetes_cluster)

        # Check OSV scanning was called
        mock_product_filter.assert_called_once_with(osv_enabled=True, automatic_osv_scanning_enabled=True)
        mock_scan_product.assert_called_once_with(mock_product)

    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.scan_product")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.api_import_observations")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Product.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Api_Configuration.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Settings.load")
    def test_task_api_import_api_disabled(
        self,
        mock_settings_load,
        mock_api_config_filter,
        mock_product_filter,
        mock_api_import_observations,
        mock_scan_product,
    ):
        # Setup
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.feature_automatic_api_import = False
        mock_settings.feature_automatic_osv_scanning = True
        mock_settings_load.return_value = mock_settings

        # Mock products
        mock_product = MagicMock()
        mock_product_filter.return_value = [mock_product]

        # Mock import results
        mock_scan_product.return_value = (4, 5, 6)  # new, updated, resolved

        # Execute
        task_api_import()

        # Assert
        # Check API import was not called
        mock_api_config_filter.assert_not_called()
        mock_api_import_observations.assert_not_called()

        # Check OSV scanning was called
        mock_product_filter.assert_called_once_with(osv_enabled=True, automatic_osv_scanning_enabled=True)
        mock_scan_product.assert_called_once_with(mock_product)

    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.scan_product")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.api_import_observations")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Product.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Api_Configuration.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Settings.load")
    def test_task_api_import_osv_disabled(
        self,
        mock_settings_load,
        mock_api_config_filter,
        mock_product_filter,
        mock_api_import_observations,
        mock_scan_product,
    ):
        # Setup
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.feature_automatic_api_import = True
        mock_settings.feature_automatic_osv_scanning = False
        mock_settings_load.return_value = mock_settings

        # Mock API configurations
        mock_api_config = MagicMock()
        mock_api_config_filter.return_value = [mock_api_config]

        # Mock import results
        mock_api_import_observations.return_value = (1, 2, 3)  # new, updated, resolved

        # Execute
        task_api_import()

        # Assert
        # Check API import was called
        mock_api_config_filter.assert_called_once_with(automatic_import_enabled=True)
        mock_api_import_observations.assert_called_once()

        # Check OSV scanning was not called
        mock_product_filter.assert_not_called()
        mock_scan_product.assert_not_called()

    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.handle_task_exception")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.api_import_observations")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Api_Configuration.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Settings.load")
    def test_task_api_import_api_exception_handling(
        self,
        mock_settings_load,
        mock_api_config_filter,
        mock_api_import_observations,
        mock_handle_task_exception,
    ):
        # Setup
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.feature_automatic_api_import = True
        mock_settings.feature_automatic_osv_scanning = False
        mock_settings_load.return_value = mock_settings

        # Mock API configurations
        mock_api_config = MagicMock()
        mock_api_config_filter.return_value = [mock_api_config]

        # Mock API import to raise exception
        test_exception = Exception("Test API import exception")
        mock_api_import_observations.side_effect = test_exception

        # Execute
        task_api_import()

        # Assert
        # Check exception was handled
        mock_handle_task_exception.assert_called_once_with(test_exception, product=mock_api_config.product)

    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.handle_task_exception")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.scan_product")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Product.objects.filter")
    @patch("application.background_tasks.periodic_tasks.import_observations_tasks.Settings.load")
    def test_task_api_import_osv_exception_handling(
        self,
        mock_settings_load,
        mock_product_filter,
        mock_scan_product,
        mock_handle_task_exception,
    ):
        # Setup
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.feature_automatic_api_import = False
        mock_settings.feature_automatic_osv_scanning = True
        mock_settings_load.return_value = mock_settings

        # Mock products
        mock_product = MagicMock()
        mock_product_filter.return_value = [mock_product]

        # Mock scan_product to raise exception
        test_exception = Exception("Test OSV scanning exception")
        mock_scan_product.side_effect = test_exception

        # Execute
        task_api_import()

        # Assert
        # Check exception was handled
        mock_handle_task_exception.assert_called_once_with(test_exception, product=mock_product)
