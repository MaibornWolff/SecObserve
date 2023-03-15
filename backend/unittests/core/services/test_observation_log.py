from unittest.mock import patch

from application.core.services.observation_log import create_observation_log
from unittests.base_test_case import BaseTestCase


class TestObservationLog(BaseTestCase):
    @patch("application.core.models.Observation.save")
    @patch("application.core.models.Observation_Log.save")
    @patch("application.core.services.observation_log.get_current_user")
    def test_create_observation_log(
        self, mock_user, mock_observation_log_save, mock_observation_save
    ):
        mock_user.return_value = self.user_internal

        observation_log = create_observation_log(
            self.observation_1, "severity", "status", "comment"
        )

        self.assertEqual(self.observation_1, observation_log.observation)
        self.assertEqual(self.user_internal, observation_log.user)
        self.assertEqual("severity", observation_log.severity)
        self.assertEqual("status", observation_log.status)

        self.assertEqual(
            self.observation_1.last_observation_log, observation_log.created
        )

        observation_log.save.assert_called_once()
        self.observation_1.save.assert_called_once()
        mock_user.assert_called_once()
