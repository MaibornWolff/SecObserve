from os import path

from application.core.types import Severity
from application.import_observations.parsers.ocsf.parser import OCSFParser
from unittests.base_test_case import BaseTestCase


class TestOCSFParser(BaseTestCase):
    def test_invalid_format_json(self):
        with open(path.dirname(__file__) + "/files/invalid_format.json") as testfile:
            parser = OCSFParser()

            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertEqual("File is not valid JSON", messages[0])
            self.assertFalse(data)

    def test_invalid_not_a_list(self):
        with open(
            path.dirname(__file__) + "/files/invalid_not_a_list.json"
        ) as testfile:
            parser = OCSFParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertIn("File is not a OCSF format, data is not a list", messages[0])
            self.assertFalse(data)

    def test_invalid_no_finding_info(self):
        with open(
            path.dirname(__file__) + "/files/invalid_no_finding_info.json"
        ) as testfile:
            parser = OCSFParser()
            check, messages, data = parser.check_format(testfile)

            self.assertFalse(check)
            self.assertIn(
                "File is not a OCSF format, first element doesn't have a finding_info entry",
                messages[0],
            )
            self.assertFalse(data)

    def test_no_observation(self):
        with open(path.dirname(__file__) + "/files/no_observation.json") as testfile:
            parser = OCSFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_other_finding(self):
        with open(path.dirname(__file__) + "/files/other_finding.json") as testfile:
            parser = OCSFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(0, len(observations))

    def test_prowler_multiple_findings(self):
        with open(
            path.dirname(__file__) + "/files/prowler_multiple_findings.json"
        ) as testfile:
            parser = OCSFParser()
            check, messages, data = parser.check_format(testfile)
            observations = parser.get_observations(data)

            self.assertTrue(check)
            self.assertEqual(0, len(messages))
            self.assertEqual(2, len(observations))

            observation = observations[0]
            self.assertEqual("Prowler / 4.3.5", observation.scanner)
            self.assertEqual(
                "Ensure clusters are created with Private Endpoint Enabled and Public Access Disabled",
                observation.title,
            )
            description = """Disable access to the Kubernetes API from outside the node network if it is not required.

**Status detail:** Public access to nodes is enabled for cluster 'aks-dev' in subscription 'Test Subscription'

**Risk details:** In a private cluster, the master node has two endpoints, a private and public endpoint. The private endpoint is the internal IP address of the master, behind an internal load balancer in the master's wirtual network. Nodes communicate with the master using the private endpoint. The public endpoint enables the Kubernetes API to be accessed from outside the master's virtual network. Although Kubernetes API requires an authorized token to perform sensitive actions, a vulnerability could potentially expose the Kubernetes publically with unrestricted access. Additionally, an attacker may be able to identify the current cluster and Kubernetes API version and determine whether it is vulnerable to an attack. Unless required, disabling public endpoint will help prevent such threats, and require the attacker to be on the master's virtual network to perform any attack on the Kubernetes API."""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "To use a private endpoint, create a new private endpoint in your virtual network then create a link between your virtual network and a new private DNS zone",
                observation.recommendation,
            )
            self.assertEqual(Severity.SEVERITY_HIGH, observation.parser_severity)
            self.assertEqual("Azure", observation.origin_cloud_provider)
            self.assertEqual(
                "Test Subscription",
                observation.origin_cloud_account_subscription_project,
            )
            self.assertEqual("aks-dev", observation.origin_cloud_resource)
            self.assertEqual(
                "Microsoft.ContainerService/ManagedClusters",
                observation.origin_cloud_resource_type,
            )
            self.assertEqual("", observation.origin_kubernetes_cluster)
            self.assertEqual("", observation.origin_kubernetes_namespace)
            self.assertEqual("", observation.origin_kubernetes_resource_type)
            self.assertEqual("", observation.origin_kubernetes_resource_name)
            self.assertEqual(2, len(observation.unsaved_references))
            self.assertEqual(
                "https://learn.microsoft.com/en-us/azure/aks/private-clusters?tabs=azure-portal",
                observation.unsaved_references[0],
            )
            self.assertEqual(
                "https://learn.microsoft.com/en-us/azure/aks/access-private-cluster?tabs=azure-cli",
                observation.unsaved_references[1],
            )
            self.assertEqual("OCSF Finding", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"uid": "prowler-azure-aks_clusters_public_access_disabled-6c63340e-8a77-447a-9a9f-6c8277e6bc83-westeurope-aks-dev"',
                observation.unsaved_evidences[0][1],
            )

            observation = observations[1]
            self.assertEqual("Prowler / 4.3.5", observation.scanner)
            self.assertEqual(
                "Ensure that the admission control plugin AlwaysPullImages is set",
                observation.title,
            )
            description = """This check verifies that the AlwaysPullImages admission control plugin is enabled in the Kubernetes API server. This plugin ensures that every new pod always pulls the required images, enforcing image access control and preventing the use of possibly outdated or altered images.

**Status detail:** AlwaysPullImages admission control plugin is not set in pod kube-apiserver-minikube.

**Risk details:** Without AlwaysPullImages, once an image is pulled to a node, any pod can use it without any authorization check, potentially leading to security risks.

**Notes:** Enabling AlwaysPullImages can increase network and registry load and decrease container startup speed. It may not be suitable for all environments."""
            self.assertEqual(description, observation.description)
            self.assertEqual(
                "Configure the API server to use the AlwaysPullImages admission control plugin to ensure image security and integrity.",
                observation.recommendation,
            )
            self.assertEqual(Severity.SEVERITY_MEDIUM, observation.parser_severity)
            self.assertEqual("", observation.origin_cloud_provider)
            self.assertEqual("", observation.origin_cloud_account_subscription_project)
            self.assertEqual("", observation.origin_cloud_resource)
            self.assertEqual("", observation.origin_cloud_resource_type)
            self.assertEqual("", observation.origin_kubernetes_cluster)
            self.assertEqual("kube-system", observation.origin_kubernetes_namespace)
            self.assertEqual(
                "KubernetesAPIServer", observation.origin_kubernetes_resource_type
            )
            self.assertEqual(
                "kube-apiserver-minikube", observation.origin_kubernetes_resource_name
            )
            self.assertEqual(3, len(observation.unsaved_references))
            self.assertEqual("OCSF Finding", observation.unsaved_evidences[0][0])
            self.assertIn(
                '"uid": "prowler-kubernetes-apiserver_always_pull_images_plugin-minikube-namespace: kube-system-kube-apiserver-minikube"',
                observation.unsaved_evidences[0][1],
            )
