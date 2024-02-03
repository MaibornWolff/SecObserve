from unittest.mock import call, patch

from application.core.models import Observation, Potential_Duplicate
from application.core.services.potential_duplicates import (
    set_potential_duplicate,
    set_potential_duplicate_both_ways,
)
from application.core.types import Status
from unittests.base_test_case import BaseTestCase


class TestSetPotentialDuplicate(BaseTestCase):
    def setUp(self):
        self.observation = Observation()
        self.observation.current_status = Status.STATUS_OPEN
        self.observation.has_potential_duplicates = True
        super().setUp()

    @patch("application.core.services.potential_duplicates.set_potential_duplicate")
    @patch("application.core.models.Potential_Duplicate.objects.filter")
    def test_set_potential_duplicate_both_ways(
        self, filter_mock, set_potential_duplicate_mock
    ):
        potential_duplicate_observation = Observation(
            title="observation_2", product=self.product_1
        )

        potential_duplicate = Potential_Duplicate()
        potential_duplicate.observation = self.observation_1
        potential_duplicate.potential_duplicate_observation = (
            potential_duplicate_observation
        )

        filter_mock.return_value = [potential_duplicate]

        set_potential_duplicate_both_ways(self.observation)

        self.assertEqual(set_potential_duplicate_mock.call_count, 2)
        # set_potential_duplicate_mock.assert_has_calls([call(self.observation_1), call(potential_duplicate_observation)])

    @patch("application.core.models.Potential_Duplicate.objects.filter")
    @patch("application.core.models.Observation.save")
    def test_set_potential_duplicate_no_open_duplicates(self, save_mock, filter_mock):
        filter_mock.return_value.count.return_value = 0

        set_potential_duplicate(self.observation)

        self.assertFalse(self.observation.has_potential_duplicates)
        save_mock.assert_called_once()

    @patch("application.core.models.Potential_Duplicate.objects.filter")
    @patch("application.core.models.Observation.save")
    def test_set_potential_duplicate_with_open_duplicates(self, save_mock, filter_mock):
        filter_mock.return_value.count.return_value = 2

        set_potential_duplicate(self.observation)

        self.assertTrue(self.observation.has_potential_duplicates)
        save_mock.assert_not_called()

    @patch("application.core.models.Observation.save")
    def test_set_potential_duplicate_closed_observation(self, save_mock):
        self.observation.current_status = Status.STATUS_RESOLVED

        set_potential_duplicate(self.observation)

        self.assertFalse(self.observation.has_potential_duplicates)
        save_mock.assert_called_once()
