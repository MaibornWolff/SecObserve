from os import path
from unittest import TestCase

from application.import_observations.parsers.trivy_prometheus.parser import TrivyPrometheus


class TestTrivyPrometheusParser(TestCase):
    def test_no_json(self):
        pass