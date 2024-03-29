from unittest.mock import call, patch

from django.core.management import call_command

from application.core.models import Observation
from application.epss.models import EPSS_Score
from application.epss.services.epss import (
    epss_apply_observation,
    epss_apply_observations,
)
from unittests.base_test_case import BaseTestCase


class TestEPSS(BaseTestCase):
    @classmethod
    @patch("application.core.signals.get_current_user")
    def setUpClass(self, mock_user):
        mock_user.return_value = None
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")
        self.maxDiff = None
        super().setUpClass()

    @patch("application.core.models.Observation.objects.filter")
    @patch("application.epss.services.epss.epss_apply_observation")
    def test_epss_apply_observations(
        self, mock_epss_apply_observation, mock_observations
    ):
        mock_observations.return_value = Observation.objects.all()
        epss_apply_observations()
        mock_observations.assert_called_with(vulnerability_id__startswith="CVE-")
        mock_epss_apply_observation.assert_has_calls(
            [call(Observation.objects.all()[0]), call(Observation.objects.all()[1])]
        )

    @patch("application.epss.models.EPSS_Score.objects.filter")
    @patch("application.core.models.Observation.save")
    def test_epss_apply_observation_not_cve(
        self, mock_observation_save, mock_epss_score
    ):
        epss_apply_observation(Observation.objects.all()[0])
        mock_epss_score.assert_not_called()
        mock_observation_save.assert_not_called()

    @patch("application.epss.models.EPSS_Score.objects.get")
    @patch("application.core.models.Observation.save")
    def test_epss_apply_observation_no_epss(
        self, mock_observation_save, mock_epss_score
    ):
        mock_epss_score.side_effect = EPSS_Score.DoesNotExist()
        cve_observation = Observation(vulnerability_id="CVE-2020-1234")

        epss_apply_observation(cve_observation)

        mock_epss_score.assert_called_with(cve="CVE-2020-1234")
        mock_observation_save.assert_not_called()

    @patch("application.epss.models.EPSS_Score.objects.get")
    @patch("application.core.models.Observation.save")
    def test_epss_apply_observation_cve(
        self, mock_observation_save, mock_epss_score_get
    ):
        mock_epss_score_get.return_value = EPSS_Score(
            cve="CVE-2020-1234", epss_score=1, epss_percentile=1
        )
        cve_observation = Observation(vulnerability_id="CVE-2020-1234")

        epss_apply_observation(cve_observation)

        self.assertEqual(cve_observation.epss_score, 100)
        self.assertEqual(cve_observation.epss_percentile, 100)
        mock_epss_score_get.assert_called_with(cve="CVE-2020-1234")
        mock_observation_save.assert_called_once()
