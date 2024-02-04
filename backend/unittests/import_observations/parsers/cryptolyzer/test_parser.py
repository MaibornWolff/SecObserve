from os import path
from unittest import TestCase

from application.core.types import Severity
from application.import_observations.parsers.cryptolyzer.parser import CryptoLyzerParser


class TestCryptolyzeParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = CryptoLyzerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.json") as testfile:
            parser = CryptoLyzerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not a valid CryptoLyzer format", messages[0])
            self.assertFalse(data)

    def test_no_observations(self):
        with open(path.dirname(__file__) + "/files/no_observations.json") as testfile:
            parser = CryptoLyzerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_multiple_observations(self):
        with open(
            path.dirname(__file__) + "/files/multiple_observations.json"
        ) as testfile:
            parser = CryptoLyzerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(4, len(observations))

            observation = observations[0]
            self.assertEqual("Unrecommended TLS 1.2 cipher suites", observation.title)
            self.assertEqual(
                "**Unrecommended cipher suites according to BSI recommendations:**\n* TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
                observation.description,
            )
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://www.example.org:443", observation.origin_endpoint_url
            )
            self.assertEqual("CryptoLyzer", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
                observation.unsaved_evidences[0][1],
            )

            observation = observations[1]
            self.assertEqual("Unrecommended TLS 1.3 cipher suites", observation.title)
            self.assertEqual(
                "**Unrecommended cipher suites according to BSI recommendations:**\n* TLS_CHACHA20_POLY1305_SHA256",
                observation.description,
            )
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://www.example.org:443", observation.origin_endpoint_url
            )
            self.assertEqual("CryptoLyzer", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "TLS_CHACHA20_POLY1305_SHA256", observation.unsaved_evidences[0][1]
            )

            observation = observations[2]
            self.assertEqual("Unrecommended elliptic curves", observation.title)
            self.assertEqual(
                "**Unrecommended elliptic curves according to BSI recommendations:**\n* X25519\n* X448",
                observation.description,
            )
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://www.example.org:443", observation.origin_endpoint_url
            )
            self.assertEqual("CryptoLyzer", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("X25519", observation.unsaved_evidences[0][1])

            observation = observations[3]
            self.assertEqual("Unrecommended signature algorithms", observation.title)
            self.assertEqual(
                "**Unrecommended signature algorithms according to BSI recommendations:**\n* RSA_SHA1\n* RSA_SHA224",
                observation.description,
            )
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://www.example.org:443", observation.origin_endpoint_url
            )
            self.assertEqual("CryptoLyzer", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("RSA_SHA224", observation.unsaved_evidences[0][1])

    def test_weak_tls(self):
        with open(path.dirname(__file__) + "/files/tls10.json") as testfile:
            parser = CryptoLyzerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(3, len(observations))

            observation = observations[0]
            self.assertEqual("Weak protocols detected", observation.title)
            self.assertEqual(
                "**Weak protocols according to BSI recommendations:**\n* tls1\n* tls1_1",
                observation.description,
            )
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://tls-v1-0.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("CryptoLyzer", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("tls1_1", observation.unsaved_evidences[0][1])
