from os import path
from unittest import TestCase

from application.core.models import Product
from application.core.types import Severity
from application.import_observations.parsers.drheader.parser import DrHEADerParser
from application.import_observations.services.parser_detector import detect_parser


class TestCycloneDXParser(TestCase):
    def test_drheader(self):
        with open(path.dirname(__file__) + "/files/drheader.json") as testfile:
            parser, parser_instance, data = detect_parser(testfile)
            self.assertEqual("DrHeader", parser.name)
            self.assertTrue(isinstance(parser_instance, DrHEADerParser))

            observations = parser_instance.get_observations(
                data, Product(name="product"), None
            )
            self.assertEqual(6, len(observations))

            observation = observations[1]
            self.assertEqual("Header: Pragma", observation.title)
            description = """Header not included in response

**Expected:** no-cache"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Pragma",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"message": "Header not included in response"',
                observation.unsaved_evidences[0][1],
            )

            observation = observations[2]
            self.assertEqual("Header: Referrer-Policy", observation.title)
            description = """Value does not match security policy. Exactly one of the expected items was expected

**Value:** same-origin

**Expected:**
* strict-origin
* strict-origin-when-cross-origin
* no-referrer"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#referrer-policy",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"message": "Value does not match security policy. Exactly one of the expected items was expected"',
                observation.unsaved_evidences[0][1],
            )

            observation = observations[4]
            self.assertEqual("Header: Strict-Transport-Security", observation.title)
            description = """Header not included in response

**Expected:** max-age=31536000; includeSubDomains"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"message": "Header not included in response"',
                observation.unsaved_evidences[0][1],
            )
