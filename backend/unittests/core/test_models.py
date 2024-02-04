from unittest.mock import patch

from application.core.models import Observation, Parser, Product
from application.core.types import Severity, Status
from unittests.base_test_case import BaseTestCase


class TestProduct(BaseTestCase):
    def test_str(self):
        product = Product(name="product_name")
        self.assertEqual("product_name", str(product))

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_critical(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_critical_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_CRITICAL,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_high(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_high_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_HIGH,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_medium(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_medium_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_MEDIUM,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_low(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_low_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_LOW,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_none(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_none_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_NONE,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_observation_count_unkown(self, mock):
        mock.return_value.count.return_value = 99
        product = Product(name="product_name")
        self.assertEqual(99, product.open_unkown_observation_count)
        mock.assert_called_with(
            product=product,
            branch=None,
            current_severity=Severity.SEVERITY_UNKOWN,
            current_status=Status.STATUS_OPEN,
        )


class TestParser(BaseTestCase):
    def test_str(self):
        parser = Parser(name="parser_name")
        self.assertEqual("parser_name", str(parser))


class TestObservation(BaseTestCase):
    def test_str(self):
        product = Product(name="product_name")
        observation = Observation(title="observation_title", product=product)
        self.assertEqual("product_name / observation_title", str(observation))

    @patch("application.core.models.normalize_observation_fields")
    @patch("application.core.models.get_identity_hash")
    @patch("django.db.models.Model.save")
    def test_save(self, save_mock, hash_mock, normalize_mock):
        hash_mock.return_value = "hash"

        product = Product(name="product_name")
        observation = Observation(title="observation_title", product=product)
        observation.save()

        self.assertEqual("hash", observation.identity_hash)
        save_mock.assert_called()
        hash_mock.assert_called_with(observation)
        normalize_mock.assert_called_with(observation)
