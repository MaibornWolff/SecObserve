import json
from os import path
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests

from application.import_observations.models import Api_Configuration
from application.import_observations.parsers.trivy_operator_prometheus.parser import (
    TrivyOperatorPrometheus,
)


class TestTrivyOperatorPrometheusParser(TestCase):
    @patch(
        "application.import_observations.parsers.trivy_operator_prometheus.parser.requests"
    )
    def test_invalid_connection(self, mock_requests):
        parser = TrivyOperatorPrometheus()

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_requests.get.return_value = mock_response
        mock_requests.get.side_effect = requests.exceptions.ConnectionError()

        result, messages, data = parser.check_connection(Api_Configuration())
        self.assertFalse(result)

        self.assertIn("Cannot access Prometheus", messages[0])
        self.assertFalse(data)

    @patch(
        "application.import_observations.parsers.trivy_operator_prometheus.parser.requests"
    )
    def test_valid_connection(self, mock_requests):
        parser = TrivyOperatorPrometheus()
        with open(
            path.dirname(__file__) + "/files/multiple_observations.json"
        ) as testfile:
            json_data = json.load(testfile)

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = json_data
            mock_requests.get.return_value = mock_response

            result, messages, data = parser.check_connection(Api_Configuration())

            self.assertEqual(result, True)
            self.assertFalse(messages)
            self.assertEqual(json_data, data)

    def test_invalid_format_json(self):
        with open(path.dirname(__file__) + "/files/invalid_format.json") as testfile:
            parser = TrivyOperatorPrometheus()

            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual("Data is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_no_prometheus_endpoint_json(self):
        with open(
            path.dirname(__file__) + "/files/no_prometheus_endpoint.json"
        ) as testfile:
            parser = TrivyOperatorPrometheus()

            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertIn("Data is not a Prometheus API-Endpoint", messages[0])
            self.assertFalse(data)

    def test_invalid_metric_endpoint_json(self):
        with open(
            path.dirname(__file__) + "/files/invalid_metric_endpoint.json"
        ) as testfile:
            parser = TrivyOperatorPrometheus()

            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            print(messages[0])
            self.assertIn("Data not in valid Prometheus-Metric Format", messages[0])
            self.assertFalse(data)

    def test_multiple_observations(self):
        with open(
            path.dirname(__file__) + "/files/multiple_observations.json"
        ) as testfile:
            parser = TrivyOperatorPrometheus()

            parser.api_configuration = Api_Configuration(
                base_url="https://prometheus.example.com"
            )
            observations = parser.get_observations(json.load(testfile))

            self.assertEqual(2, len(observations))
            self.assertEqual("CVE-2023-1111", observations[0].title)
            self.assertEqual("Medium", observations[0].parser_severity)
            self.assertEqual("6.1", observations[0].numerical_severity)
            self.assertEqual("CVE-2023-1111", observations[0].vulnerability_id)
            self.assertEqual(
                "registry.io/namespace/image", observations[0].origin_docker_image_name
            )
            self.assertEqual("v0.26.0", observations[0].origin_docker_image_tag)
            self.assertEqual("6.1", observations[0].cvss3_score)
            self.assertEqual("recoure.org/x/net", observations[0].origin_component_name)
            self.assertEqual("Trivy Operator", observations[0].scanner)
            self.assertEqual(
                "Upgrade from **v0.10.0** to **0.1.0**",
                observations[0].recommendation,
            )
            self.assertEqual(
                "very vulnerable\n\n**Prometheus host:** https://prometheus.example.com",
                observations[0].description,
            )
            self.assertEqual("default", observations[0].origin_kubernetes_namespace)
            self.assertEqual(
                "StatefulSet", observations[0].origin_kubernetes_resource_type
            )
            self.assertEqual(
                "recource_name", observations[0].origin_kubernetes_resource_name
            )
