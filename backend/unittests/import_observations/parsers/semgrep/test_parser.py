from os import path
from unittest import TestCase

from application.import_observations.parsers.semgrep.parser import SemgrepParser


class TestSemgrepParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = SemgrepParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.json") as testfile:
            parser = SemgrepParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not a Semgrep format, version is missing", messages[0]
            )
            self.assertFalse(data)

    def test_no_observation(self):
        with open(path.dirname(__file__) + "/files/no_observation.json") as testfile:
            parser = SemgrepParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_multiple_observations(self):
        with open(
            path.dirname(__file__) + "/files/multiple_observations.json"
        ) as testfile:
            parser = SemgrepParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(3, len(observations))

            observation = observations[0]
            self.assertEqual(
                "python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query",
                observation.title,
            )
            description = """Avoiding SQL string concatenation: untrusted input concatenated with raw SQL query can result in SQL Injection. In order to execute raw query safely, prepared statement should be used. SQLAlchemy provides TextualSQL to easily used prepared statement with named parameters. For complex SQL composition, use SQL Expression Language or Schema Definition Language. In most cases, SQLAlchemy ORM will be a better option.

**Vulnerability Class:** SQL Injection"""
            self.assertEqual(description, observation.description)
            self.assertEqual(None, observation.recommendation)
            self.assertEqual("High", observation.parser_severity)
            self.assertEqual(
                "application/management/commands/command.py",
                observation.origin_source_file,
            )
            self.assertEqual(62, observation.origin_source_line_start)
            self.assertEqual(62, observation.origin_source_line_end)
            self.assertEqual("Semgrep (OSS) / 1.100.0", observation.scanner)
            self.assertEqual(4, len(observation.unsaved_references))
            self.assertEqual(
                "https://semgrep.dev/r/python.sqlalchemy.security.sqlalchemy-execute-raw-query.sqlalchemy-execute-raw-query",
                observation.unsaved_references[0],
            )
            self.assertEqual(
                "https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql",
                observation.unsaved_references[1],
            )
            self.assertEqual(1, len(observation.unsaved_evidences))
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("oqUz5y", observation.unsaved_evidences[0][1])

            observation = observations[1]
            self.assertEqual(
                "python.lang.security.insecure-hash-algorithms-md5.insecure-hash-algorithm-md5",
                observation.title,
            )
            description = """Detected MD5 hash algorithm which is considered insecure. MD5 is not collision resistant and is therefore not suitable as a cryptographic signature. Use SHA256 or SHA3 instead.

**Vulnerability Classes:** Cryptographic Issues, Other Issues"""
            self.assertEqual(description, observation.description)
            self.assertEqual(None, observation.recommendation)
            self.assertEqual("Medium", observation.parser_severity)

            observation = observations[2]
            self.assertEqual(
                "python.lang.security.use-defusedcsv.use-defusedcsv", observation.title
            )
            recommendation = """```
defusedcsv.writer(open(file_path, 'w'))
```"""
            self.assertEqual(recommendation, observation.recommendation)
            self.assertEqual("Low", observation.parser_severity)
