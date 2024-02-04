from os import path
from unittest import TestCase

from application.core.types import Severity
from application.import_observations.parsers.drheader.parser import DrHEADerParser


class TestCycloneDXParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = DrHEADerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format_1(self):
        with open(path.dirname(__file__) + "/files/wrong_format_1.json") as testfile:
            parser = DrHEADerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not a DrHeader format, data is not a list", messages[0]
            )
            self.assertFalse(data)

    def test_wrong_format_2(self):
        with open(path.dirname(__file__) + "/files/wrong_format_2.json") as testfile:
            parser = DrHEADerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "Data is not a DrHeader format, element doesn't have a rule entry",
                messages[0],
            )
            self.assertFalse(data)

    def test_drheader(self):
        with open(path.dirname(__file__) + "/files/drheader.json") as testfile:
            parser = DrHEADerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
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
