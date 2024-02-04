from os import path
from unittest import TestCase

from application.core.types import Severity
from application.import_observations.parsers.prowler.parser import ProwlerParser


class TestProwlerParser(TestCase):
    def test_no_json(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_wrong_format_1(self):
        with open(path.dirname(__file__) + "/files/wrong_format_1.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not a Prowler format, data is not a list", messages[0]
            )
            self.assertFalse(data)

    def test_wrong_format_2(self):
        with open(path.dirname(__file__) + "/files/wrong_format_2.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "File is not a Prowler format, element is not a dictionary", messages[0]
            )
            self.assertFalse(data)

    def test_wrong_format_3(self):
        with open(path.dirname(__file__) + "/files/wrong_format_3.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual(
                "Data is not a Prowler format, element doesn't have a StatusExtended or Status entry",
                messages[0],
            )
            self.assertFalse(data)

    def test_no_observations(self):
        with open(path.dirname(__file__) + "/files/no_observations.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_aws(self):
        with open(path.dirname(__file__) + "/files/prowler_aws.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(1, len(observations))

            observation = observations[0]
            self.assertEqual(
                "RDS Instance rds-instance-id has minor version upgrade enabled.",
                observation.title,
            )
            description = """Ensure RDS instances have minor version upgrade enabled.

Auto Minor Version Upgrade is a feature that you can enable to have your database automatically upgraded when a new minor database engine version is available. Minor version upgrades often patch security vulnerabilities and fix bugs and therefore should be applied."""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_LOW, observation.parser_severity)
            self.assertIn(
                "Enable auto minor version upgrade for all databases and environments.",
                observation.recommendation,
            )
            self.assertIn(
                "* https://aws.amazon.com/blogs/database/best-practices-for-upgrading-amazon-rds-to-major-and-minor-versions-of-postgresql/",
                observation.recommendation,
            )
            self.assertIn(
                "* **NativeIaC:** https://docs.bridgecrew.io/docs/ensure-aws-db-instance-gets-all-minor-upgrades-automatically#cloudformation",
                observation.recommendation,
            )
            self.assertEqual("AWS", observation.origin_cloud_provider)
            self.assertEqual(
                "ACCOUNT_ID", observation.origin_cloud_account_subscription_project
            )
            self.assertEqual("rds-instance-id", observation.origin_cloud_resource)
            self.assertEqual("AwsRdsDbInstance", observation.origin_cloud_resource_type)
            self.assertEqual(
                "https://aws.amazon.com/blogs/database/best-practices-for-upgrading-amazon-rds-to-major-and-minor-versions-of-postgresql/",
                observation.unsaved_references[0],
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("eu-west-1", observation.unsaved_evidences[0][1])

    def test_azure(self):
        with open(path.dirname(__file__) + "/files/prowler_azure.json") as testfile:
            parser = ProwlerParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(2, len(observations))

            observation = observations[0]
            self.assertEqual(
                "Defender plan Defender for App Services from subscription Example_Subscription - XAKS is set to OFF (pricing tier not standard)",
                observation.title,
            )
            description = """Ensure That Microsoft Defender for App Services Is Set To 'On' 

Turning on Microsoft Defender for App Service enables threat detection for App Service, providing threat intelligence, anomaly detection, and behavior analytics in the Microsoft Defender for Cloud."""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            recommendation = """By default, Microsoft Defender for Cloud is not enabled for your App Service instances. Enabling the Defender security service for App Service instances allows for advanced security defense using threat detection capabilities provided by Microsoft Security Response Center.

* **Terraform:** https://docs.bridgecrew.io/docs/ensure-that-azure-defender-is-set-to-on-for-app-service#terraform

* **CLI:** https://www.trendmicro.com/cloudoneconformity/knowledge-base/azure/SecurityCenter/defender-app-service.html

* **Other:** https://www.trendmicro.com/cloudoneconformity/knowledge-base/azure/SecurityCenter/defender-app-service.html"""
            self.assertEqual(recommendation, observation.recommendation)
            self.assertEqual("Azure", observation.origin_cloud_provider)
            self.assertEqual(
                "Example_Subscription - XAKS",
                observation.origin_cloud_account_subscription_project,
            )
            self.assertEqual(
                "Defender plan App Services", observation.origin_cloud_resource
            )
            self.assertEqual(
                "AzureDefenderPlan", observation.origin_cloud_resource_type
            )
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn(
                "defender_ensure_defender_for_app_services_is_on",
                observation.unsaved_evidences[0][1],
            )
