from os import path
from unittest import TestCase

from application.core.types import Severity
from application.import_observations.parsers.sarif.parser import SARIFParser


class TestSarifParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format_1(self):
        with open(path.dirname(__file__) + "/files/wrong_format_1.json") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not SARIF format, 'version' and/or '$schema' are missing",
                messages[0],
            )
            self.assertFalse(data)

    def test_wrong_format_2(self):
        with open(path.dirname(__file__) + "/files/wrong_format_2.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not SARIF format, version is not 2.1.0", messages[0]
            )
            self.assertFalse(data)

    def test_checkov(self):
        with open(path.dirname(__file__) + "/files/checkov.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(4, len(observations))

            observation = observations[0]
            self.assertEqual("Checkov / 2.1.277", observation.scanner)
            self.assertEqual(
                "Ensure that HEALTHCHECK instructions have been added to container images",
                observation.title,
            )
            description = """Ensure that HEALTHCHECK instructions have been added to container images

"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "frontend/docker/Dockerfile", observation.origin_source_file
            )
            self.assertEqual(1, observation.origin_source_line_start)
            self.assertEqual(41, observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://docs.bridgecrew.io/docs/ensure-that-healthcheck-instructions-have-been-added-to-container-images",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn('"id": "CKV_DOCKER_2"', observation.unsaved_evidences[0][1])
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn(
                '"ruleId": "CKV_DOCKER_2"', observation.unsaved_evidences[1][1]
            )

    def test_eslint(self):
        with open(path.dirname(__file__) + "/files/eslint.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(5, len(observations))

            observation = observations[0]
            self.assertEqual("ESLint / 8.25.0", observation.scanner)
            self.assertEqual("@typescript-eslint/no-unused-vars", observation.title)
            description = """'locale' is defined but never used.

**Rule short description:** Disallow unused variables

"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "file:///home/stefanf/workspace/SecObserve/frontend/src/App.tsx",
                observation.origin_source_file,
            )
            self.assertEqual(19, observation.origin_source_line_start)
            self.assertEqual(19, observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://typescript-eslint.io/rules/no-unused-vars",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"id": "@typescript-eslint/no-unused-vars"',
                observation.unsaved_evidences[0][1],
            )
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn(
                '"ruleId": "@typescript-eslint/no-unused-vars"',
                observation.unsaved_evidences[1][1],
            )

    def test_bandit(self):
        with open(path.dirname(__file__) + "/files/bandit.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(2, len(observations))

            observation = observations[0]
            self.assertEqual("Bandit", observation.scanner)
            self.assertEqual("hardcoded_bind_all_interfaces", observation.title)
            description = """Possible binding to all interfaces.

**Snippet:** `ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=["localhost", "0.0.0.0", "127.0.0.1"])`

**Issue_Confidence:** MEDIUM

**Issue_Severity:** MEDIUM

"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "backend/config/settings/dist.py", observation.origin_source_file
            )
            self.assertEqual(14, observation.origin_source_line_start)
            self.assertIsNone(observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://bandit.readthedocs.io/en/1.7.4/plugins/b104_hardcoded_bind_all_interfaces.html",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn('"id": "B104"', observation.unsaved_evidences[0][1])
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn('"ruleId": "B104"', observation.unsaved_evidences[1][1])

    def test_kics(self):
        with open(path.dirname(__file__) + "/files/kics.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(2, len(observations))

            observation = observations[0]
            self.assertEqual("KICS / development", observation.scanner)
            self.assertEqual("Docker Socket Mounted In Container", observation.title)
            description = """There is a docker socket named 'docker.sock' mounted in a volume

**Rule full description:** Docker socket docker.sock should not be mounted on host. If the docker socket is mounted, it can allow its processes to execute docker commands.

"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "docker-compose-prod-postgres.yml", observation.origin_source_file
            )
            self.assertEqual(34, observation.origin_source_line_start)
            self.assertIsNone(observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual(
                "https://docs.docker.com/compose/compose-file/#volumes",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"id": "d6355c88-1e8d-49e9-b2f2-f8a1ca12c75b"',
                observation.unsaved_evidences[0][1],
            )
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn(
                '"ruleId": "d6355c88-1e8d-49e9-b2f2-f8a1ca12c75b"',
                observation.unsaved_evidences[1][1],
            )

    def test_trivy_config(self):
        with open(path.dirname(__file__) + "/files/trivy_config.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(1, len(observations))

            observation = observations[0]
            self.assertEqual("Trivy / 0.47.0", observation.scanner)
            self.assertEqual(
                "Ensure that the expiration date is set on all keys", observation.title
            )
            description = """**Rule full description:** Expiration Date is an optional Key Vault Key behavior and is not set by default.

Set when the resource will be become inactive.

**Precision:** very-high

**Security-Severity:** 5.5

**Tags:** ['misconfiguration', 'security', 'MEDIUM']

"""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "modules/azure-cosmosdb/main.tf", observation.origin_source_file
            )
            self.assertEqual(164, observation.origin_source_line_start)
            self.assertEqual(176, observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://avd.aquasec.com/misconfig/avd-azu-0014",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"id": "AVD-AZU-0014"',
                observation.unsaved_evidences[0][1],
            )
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn(
                '"ruleId": "AVD-AZU-0014"',
                observation.unsaved_evidences[1][1],
            )

    def test_dependency_check(self):
        with open(path.dirname(__file__) + "/files/dependency-check.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(3, len(observations))

            observation = observations[0]
            self.assertEqual("dependency-check / 8.0.1", observation.scanner)
            self.assertEqual("CVE-2022-42920", observation.title)
            self.assertIn(
                "CVE-2022-42920 - Apache Commons BCEL has a number of APIs",
                observation.description,
            )
            self.assertEqual("CVE-2022-42920", observation.vulnerability_id)
            self.assertEqual(9.8, observation.cvss3_score)
            self.assertEqual("org.apache.bcel:bcel", observation.origin_component_name)
            self.assertEqual("6.5.0", observation.origin_component_version)
            self.assertEqual(
                "pkg:maven/org.apache.bcel/bcel@6.5.0",
                observation.origin_component_purl,
            )
            self.assertEqual("", observation.parser_severity)

            observation = observations[1]
            self.assertEqual("CVE-2023-0044", observation.title)
            self.assertEqual(8.8, observation.cvss4_score)
            self.assertEqual(
                "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:L/SI:L/SA:N",
                observation.cvss4_vector,
            )
            self.assertEqual("", observation.parser_severity)

    def test_semgrep(self):
        with open(path.dirname(__file__) + "/files/semgrep.sarif") as testfile:
            parser = SARIFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(4, len(observations))

            observation = observations[0]
            self.assertEqual("semgrep / 1.16.0", observation.scanner)
            self.assertEqual(
                "typescript.react.portability.i18next.jsx-not-internationalized.jsx-not-internationalized",
                observation.title,
            )
            self.assertIn("JSX element not internationalized:", observation.description)
            self.assertEqual(
                "frontend/src/access_control/AADSignInButton.tsx",
                observation.origin_source_file,
            )
            self.assertEqual(27, observation.origin_source_line_start)
            self.assertEqual(33, observation.origin_source_line_end)
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "https://semgrep.dev/r/typescript.react.portability.i18next.jsx-not-internationalized.jsx-not-internationalized",
                observation.unsaved_references[0],
            )
            self.assertEqual("Rule", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"id": "typescript.react.portability.i18next.jsx-not-internationalized.jsx-not-internationalized"',
                observation.unsaved_evidences[0][1],
            )
            self.assertEqual("Result", observation.unsaved_evidences[1][0])
            self.assertIn(
                '"ruleId": "typescript.react.portability.i18next.jsx-not-internationalized.jsx-not-internationalized"',
                observation.unsaved_evidences[1][1],
            )
