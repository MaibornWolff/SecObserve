from unittest.mock import Mock, call, patch

from django.core.management import call_command
from rest_framework.exceptions import ValidationError

from application.core.models import Observation, Product
from application.core.services.observations_bulk_actions import (
    _check_observations,
    observations_bulk_assessment,
    observations_bulk_delete,
)
from unittests.base_test_case import BaseTestCase


class TestObservationsBulkActions(BaseTestCase):
    def setUp(self):
        super().setUp()
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")

    @patch("application.core.services.observations_bulk_actions._check_observations")
    @patch("application.core.services.observations_bulk_actions.save_assessment")
    def test_observations_bulk_assessment(self, save_mock, check_mock):
        observation_2 = Observation()
        check_mock.return_value = [self.observation_1, observation_2]

        observations_bulk_assessment(
            self.product_1,
            Observation.SEVERITY_CRITICAL,
            Observation.STATUS_OPEN,
            "comment",
            [1, 2],
        )

        check_mock.assert_called_with(self.product_1, [1, 2])
        expected_calls = [
            call(
                self.observation_1,
                Observation.SEVERITY_CRITICAL,
                Observation.STATUS_OPEN,
                "comment",
            ),
            call(
                observation_2,
                Observation.SEVERITY_CRITICAL,
                Observation.STATUS_OPEN,
                "comment",
            ),
        ]
        save_mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.core.services.observations_bulk_actions._check_observations")
    @patch("django.db.models.query.QuerySet.delete")
    def test_observations_bulk_assessment(self, delete_mock, check_mock):
        check_mock.return_value = Observation.objects.all()

        observations_bulk_delete(self.product_1, [1, 2])

        check_mock.assert_called_with(self.product_1, [1, 2])
        delete_mock.assert_called_once()

    @patch("application.core.models.Observation.objects.filter")
    def test_check_observations_count(self, mock):
        mock.return_value.count.return_value = 1

        with self.assertRaises(ValidationError) as e:
            _check_observations(self.product_1, [1, 2])

        self.assertEqual(
            str(e.exception),
            "[ErrorDetail(string='Some observations do not exist', code='invalid')]",
        )

    def test_check_observation_not_in_product(self):
        product_2 = Product.objects.get(pk=2)

        with self.assertRaises(ValidationError) as e:
            _check_observations(product_2, [1])

        self.assertEqual(
            str(e.exception),
            "[ErrorDetail(string='Observation 1 does not belong to product 2', code='invalid')]",
        )

    def test_check_observation_success(self):
        product_1 = Product.objects.get(pk=1)

        observations = _check_observations(product_1, [1])

        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0], Observation.objects.get(pk=1))
