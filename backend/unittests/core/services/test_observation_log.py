from unittest.mock import patch

from application.core.services.observation_log import create_observation_log
from application.core.types import Assessment_Status
from unittests.base_test_case import BaseTestCase


class TestObservationLog(BaseTestCase):
    @patch("application.core.models.Observation.save")
    @patch("application.core.models.Observation_Log.save")
    @patch("application.core.services.observation_log.get_current_user")
    @patch("application.core.models.Product.save")
    def test_create_observation_log(
        self,
        mock_product_save,
        mock_user,
        mock_observation_log_save,
        mock_observation_save,
    ):
        mock_user.return_value = self.user_internal

        observation_log = create_observation_log(
            self.observation_1,
            "severity",
            "status",
            "comment",
            "vex_justification",
            Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
        )

        self.assertEqual(self.observation_1, observation_log.observation)
        self.assertEqual(self.user_internal, observation_log.user)
        self.assertEqual("severity", observation_log.severity)
        self.assertEqual("status", observation_log.status)
        self.assertEqual("comment", observation_log.comment)
        self.assertEqual("vex_justification", observation_log.vex_justification)
        self.assertEqual(
            Assessment_Status.ASSESSMENT_STATUS_AUTO_APPROVED,
            observation_log.assessment_status,
        )

        self.assertEqual(
            self.observation_1.last_observation_log, observation_log.created
        )

        observation_log.save.assert_called_once()
        self.observation_1.save.assert_called_once()
        mock_user.assert_called_once()
        self.observation_1.product.save.assert_called_once()
