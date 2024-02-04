from os import path
from unittest import TestCase

from application.core.types import Severity
from application.import_observations.parsers.azure_defender.parser import (
    AzureDefenderParser,
)


class TestAzureDefenderParser(TestCase):
    def test_no_csv(self):
        with open(path.dirname(__file__) + "/test_parser.py") as testfile:
            parser = AzureDefenderParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not CSV", messages[0])
            self.assertFalse(data)

    def test_wrong_format(self):
        with open(path.dirname(__file__) + "/files/wrong_format.csv") as testfile:
            parser = AzureDefenderParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual(1, len(messages))
            self.assertEqual("File is not an Azure Defender export", messages[0])
            self.assertFalse(data)

    def test_no_observations_1(self):
        with open(path.dirname(__file__) + "/files/no_observations_1.csv") as testfile:
            parser = AzureDefenderParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_no_observations_2(self):
        with open(path.dirname(__file__) + "/files/no_observations_2.csv") as testfile:
            parser = AzureDefenderParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_defender(self):
        with open(
            path.dirname(__file__) + "/files/AzureSecurityCenterRecommendations.csv",
            "rb",
        ) as testfile:
            parser = AzureDefenderParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(2, len(observations))

            observation = observations[0]
            self.assertEqual(
                "Storage account should use a private link connection",
                observation.title,
            )
            description = """Private links enforce secure communication, by providing private connectivity to the storage account"""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual(
                "To enforce secure communications for your storage accounts, add a private endpoint as described here: https://aka.ms/connectprivatelytostorageaccount.",
                observation.recommendation,
            )
            self.assertEqual("Azure", observation.origin_cloud_provider)
            self.assertEqual(
                "Test Subscription",
                observation.origin_cloud_account_subscription_project,
            )
            self.assertEqual("teststorageacc", observation.origin_cloud_resource)
            self.assertEqual("storageaccounts", observation.origin_cloud_resource_type)
            self.assertEqual("Result", observation.unsaved_evidences[0][0])
            self.assertIn("test-weu-prod-rg", observation.unsaved_evidences[0][1])

            observation = observations[1]
            self.assertEqual(
                "Blocked accounts with read and write permissions on Azure resources should be removed",
                observation.title,
            )
            description = """Accounts that have been blocked from signing in on Active Directory, should be removed from your Azure resources.

These accounts can be targets for attackers looking to find ways to access your data without being noticed."""
            self.assertEqual(description, observation.description)
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            recommendation = """Review the list of accounts that are blocked from signing in on the Accounts section. Select an account to view its role definitions and locate the source scope. If you accept the risk for specific account, use the exempt capability to exclude it from evaluation.

Go to the Azure portal.

Open Access control (IAM) at a scope, such as management group, subscription, resource group, or resource, where the guest user has a role assignment.

Click the Role assignments tab to view all the role assignments.

In the list of role assignments, add a checkmark next to the blocked user with the role assignment you want to remove.

Click Remove. In the remove role assignment message that appears, click Yes."""
            self.assertEqual(recommendation, observation.recommendation)
