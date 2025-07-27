from unittest.mock import patch

from application.background_tasks.periodic_tasks.metrics_tasks import (
    task_calculate_product_metrics,
)
from unittests.base_test_case import BaseTestCase


class TestMetricsTasks(BaseTestCase):
    # ---------------------------------------------------------------
    # task_calculate_product_metrics
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.metrics_tasks.calculate_product_metrics")
    def test_task_calculate_product_metrics(self, mock_calculate_product_metrics):
        # Execute
        task_calculate_product_metrics()

        # Assert
        mock_calculate_product_metrics.assert_called_once()
