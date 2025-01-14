from os import path
from unittest import TestCase

from rest_framework.exceptions import ValidationError

from application.import_observations.services.parser_detector import detect_parser


class TestParserDetector(TestCase):
    def test_unknown_filetype(self):
        with open(path.dirname(__file__) + "/test_parser_detector.py") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='File is not CSV, JSON or SARIF', code='invalid')]",
                str(e.exception),
            )

    def test_csv_empty(self):
        with open(path.dirname(__file__) + "/files/empty.csv") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )

    def test_csv_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.csv") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )

    def test_csv_no_parser_found(self):
        with open(path.dirname(__file__) + "/files/no_parser_found.csv") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )

    def test_json_empty_list(self):
        with open(path.dirname(__file__) + "/files/empty_list.json") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )

    def test_json_empty_dict(self):
        with open(path.dirname(__file__) + "/files/empty_dict.json") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )

    def test_json_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.json") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='File is not valid JSON', code='invalid')]",
                str(e.exception),
            )

    def test_json_no_parser_found(self):
        with open(path.dirname(__file__) + "/files/no_parser_found.json") as testfile:
            with self.assertRaises(ValidationError) as e:
                _, _, _ = detect_parser(testfile)
                self.fail("Expected ValidationError not raised")
            self.assertEqual(
                "[ErrorDetail(string='No suitable parser found', code='invalid')]",
                str(e.exception),
            )
