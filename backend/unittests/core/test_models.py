from unittest.mock import patch

from application.core.models import Observation, Product
from application.import_observations.models import Parser
from unittests.base_test_case import BaseTestCase


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
