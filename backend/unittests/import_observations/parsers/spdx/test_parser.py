from os import path
from unittest import TestCase

from application.import_observations.parsers.spdx.parser import SPDXParser


class TestSPDXParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = SPDXParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.json") as testfile:
            parser = SPDXParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "Error while parsing document None: ['CreationInfo does not exist.']",
                messages[0],
            )
            self.assertFalse(data)

    def test_no_observation(self):
        with open(path.dirname(__file__) + "/files/no_observation.json") as testfile:
            parser = SPDXParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)
            license_components = parser.get_license_components(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))
            self.assertEqual(0, len(license_components))

    def test_multiple_observations(self):
        with open(
            path.dirname(__file__) + "/files/multiple_observations.json"
        ) as testfile:
            parser = SPDXParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)
            license_components = parser.get_license_components(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))
            self.assertEqual(124, len(license_components))

            license_component = license_components[1]
            self.assertEqual("", license_component.unsaved_license)
            self.assertEqual(".python-rundeps", license_component.name)
            self.assertEqual("20241001.223602", license_component.version)
            self.assertEqual(
                "pkg:apk/alpine/.python-rundeps@20241001.223602?arch=noarch&distro=3.20.3",
                license_component.purl,
            )
            dependencies = """alpine:3.20.3 --> .python-rundeps:20241001.223602
maibornwolff/secobserve-backend:1.20.0 --> alpine:3.20.3"""
            self.assertEqual(dependencies, license_component.dependencies)
            self.assertEqual(1, len(license_component.unsaved_evidences))
            self.assertEqual("Package", license_component.unsaved_evidences[0][0])
            self.assertIn(
                "SPDXRef-Package-82ad85e2f96c7331",
                license_component.unsaved_evidences[0][1],
            )

            license_component = license_components[2]
            self.assertEqual("BSD-3-Clause", license_component.unsaved_license)
            self.assertEqual("Django", license_component.name)
            self.assertEqual("", license_component.version)
            self.assertEqual(
                "pkg:pypi/django@5.1.2",
                license_component.purl,
            )
            dependencies = """maibornwolff/secobserve-backend:1.20.0 --> Django"""
            self.assertEqual(dependencies, license_component.dependencies)
            self.assertEqual(1, len(license_component.unsaved_evidences))
            self.assertEqual("Package", license_component.unsaved_evidences[0][0])
            self.assertIn(
                "SPDXRef-Package-d254ad6cee138a57",
                license_component.unsaved_evidences[0][1],
            )

            license_component = license_components[3]
            self.assertEqual("MIT", license_component.unsaved_license)
            self.assertEqual("PyJWT", license_component.name)
            self.assertEqual("2.9.0", license_component.version)

            license_component = license_components[4]
            self.assertEqual('', license_component.unsaved_license)
            self.assertEqual("PyMySQL", license_component.name)
            self.assertEqual("1.1.1", license_component.version)

            license_component = license_components[89]
            self.assertEqual("Artistic-1.0-Perl AND GPL-1.0-or-later", license_component.unsaved_license)
            self.assertEqual("perl", license_component.name)
            self.assertEqual("5.38.2-r0", license_component.version)
            self.assertEqual(
                "pkg:apk/alpine/perl@5.38.2-r0?arch=x86_64&distro=3.20.3",
                license_component.purl,
            )
            dependencies = """alpine:3.20.3 --> mariadb-client:10.11.8-r0
alpine:3.20.3 --> mysql-client:10.11.8-r0
alpine:3.20.3 --> perl:5.38.2-r0
alpine:3.20.3 --> postgresql-libs:20241014.093848
maibornwolff/secobserve-backend:1.20.0 --> alpine:3.20.3
mariadb-client:10.11.8-r0 --> perl:5.38.2-r0
mysql-client:10.11.8-r0 --> mariadb-client:10.11.8-r0
postgresql-libs:20241014.093848 --> mysql-client:10.11.8-r0"""
            self.assertEqual(dependencies, license_component.dependencies)
