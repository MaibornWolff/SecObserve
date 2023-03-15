from os import path
from unittest import TestCase
from application.import_observations.parsers.sslyze.parser import SSLyzeParser
from application.core.models import Observation


class TestSSLyzeParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = SSLyzeParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertIsNone(data)

    def test_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.json") as testfile:
            parser = SSLyzeParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not a valid SSLyze format", messages[0])
            self.assertIsNone(data)

    def test_no_observation(self):
        with open(
            path.dirname(__file__) + "/files/one_target_no_observations.json"
        ) as testfile:
            parser = SSLyzeParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_one_target_multiple_observations(self):
        with open(
            path.dirname(__file__) + "/files/one_target_multiple_observations.json"
        ) as testfile:
            parser = SSLyzeParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(6, len(observations))

            observation = observations[0]
            self.assertEqual("Unrecommended TLS 1.2 cipher suites", observation.title)
            self.assertEqual(
                "**Unrecommended cipher suites according to BSI recommendations:**\n* TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
                observation.description,
            )
            self.assertEqual(Observation.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4",
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
            self.assertEqual(Observation.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4",
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
            self.assertEqual(Observation.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("X25519", observation.unsaved_evidences[0][1])

            observation = observations[3]
            self.assertEqual("Vulnerable to Heartbleed", observation.title)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)

            observation = observations[4]
            self.assertEqual("Vulnerable to CCS Injection", observation.title)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "is_vulnerable_to_ccs_injection", observation.unsaved_evidences[0][1]
            )

            observation = observations[5]
            self.assertEqual(
                "Vulnerable to session renegotiation DoS", observation.title
            )
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual("https://example.com:443", observation.origin_endpoint_url)
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "is_vulnerable_to_client_renegotiation_dos",
                observation.unsaved_evidences[0][1],
            )

    def test_multiple_targets_multiple_observations(self):
        with open(
            path.dirname(__file__)
            + "/files/multiple_targets_multiple_observations.json"
        ) as testfile:
            parser = SSLyzeParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(22, len(observations))

            observation = observations[0]
            self.assertEqual("Certificate has expired", observation.title)
            description = """**Truststores:**
* Android / 13.0.0_r8
* Apple / iOS 15.1, iPadOS 15.1, macOS 12.1, tvOS 15.1, and watchOS 8.1
* Java / jdk-13.0.2
* Mozilla / 2022-09-18
* Windows / 2022-08-15"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://expired.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "certificate has expired", observation.unsaved_evidences[0][1]
            )

            observation = observations[1]
            self.assertEqual("TLS 1.0 protocol is outdated", observation.title)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://expired.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"is_tls_version_supported": true,', observation.unsaved_evidences[0][1]
            )

            observation = observations[2]
            self.assertEqual("TLS 1.1 protocol is outdated", observation.title)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://expired.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual(
                "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"is_tls_version_supported": true,', observation.unsaved_evidences[0][1]
            )

            observation = observations[4]
            self.assertEqual("Self signed certificate", observation.title)
            description = """**Truststores:**
* Android / 13.0.0_r8
* Apple / iOS 15.1, iPadOS 15.1, macOS 12.1, tvOS 15.1, and watchOS 8.1
* Java / jdk-13.0.2
* Mozilla / 2022-09-18
* Windows / 2022-08-15"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://self-signed.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "self signed certificate", observation.unsaved_evidences[0][1]
            )

            observation = observations[8]
            self.assertEqual(
                "Leaf certificate subject does not match hostname", observation.title
            )
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://wrong.host.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"leaf_certificate_subject_matches_hostname": false',
                observation.unsaved_evidences[0][1],
            )

            observation = observations[12]
            self.assertEqual(
                "Self signed certificate in certificate chain", observation.title
            )
            description = """**Truststores:**
* Android / 13.0.0_r8
* Apple / iOS 15.1, iPadOS 15.1, macOS 12.1, tvOS 15.1, and watchOS 8.1
* Java / jdk-13.0.2
* Mozilla / 2022-09-18
* Windows / 2022-08-15"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Observation.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://untrusted-root.badssl.com:443", observation.origin_endpoint_url
            )
            self.assertEqual("SSLyze / 5.0.6", observation.scanner)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "self signed certificate", observation.unsaved_evidences[0][1]
            )
