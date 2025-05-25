from os import path
from unittest import TestCase

from application.core.models import Product
from application.core.types import Severity
from application.import_observations.parsers.zap.parser import ZAPParser
from application.import_observations.services.parser_detector import detect_parser


class TestZAPParserParser(TestCase):
    def test_zap(self):
        with open(path.dirname(__file__) + "/files/owasp_zap.json") as testfile:
            parser, parser_instance, data = detect_parser(testfile)
            self.assertEqual("ZAP", parser.name)
            self.assertIsInstance(parser_instance, ZAPParser)

            observations, scanner = parser_instance.get_observations(data, Product(name="product"), None)

            self.assertEqual("OWASP ZAP / 2.12.0", scanner)
            self.assertEqual(5, len(observations))

            observation = observations[0]
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://vulncat.fortify.com/en/detail?id=desc.config.dotnet.html5_overly_permissive_cors_policy",
                observation.unsaved_references[0],
            )

            observation = observations[1]
            self.assertEqual("OWASP ZAP / 2.12.0", observation.scanner)
            self.assertEqual(
                "Information Disclosure - Suspicious Comments",
                observation.title,
            )
            description = """<p>The response appears to contain suspicious comments which may help an attacker. Note: Matches made within script blocks or files are against the entire content not only comments.</p>

**Other info:** <p>The following pattern was used: \\bADMIN\\b and was detected in the element starting with: "<script src=\"/django-static/admin/js/nav_sidebar.js\" defer></script>", see evidence field for the suspicious comment/snippet.</p>

**Amount of instances:** 4

**First instance:**
* **URI:** https://example-backend.example.com/admin/
* **Method:** GET
* **Evidence:** admin"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "<p>Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.</p>",
                observation.recommendation,
            )
            self.assertEqual(Severity.SEVERITY_NONE, observation.parser_severity)
            self.assertEqual("200", observation.cwe)
            self.assertEqual("https://example-backend.example.com", observation.origin_endpoint_url)
            self.assertEqual("Alert", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"alert": "Information Disclosure - Suspicious Comments"',
                observation.unsaved_evidences[0][1],
            )
