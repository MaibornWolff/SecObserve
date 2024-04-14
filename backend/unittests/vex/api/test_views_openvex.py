from os import path
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import dateparse
from rest_framework.test import APIClient

from application.access_control.models import User
from application.core.models import Observation, Product, Product_Member
from application.vex.models import OpenVEX, OpenVEX_Branch, OpenVEX_Vulnerability


class TestOpenVEX(TestCase):
    def setUp(self):
        Observation.objects.all().delete()
        Product.objects.filter(is_product_group=False).delete()
        Product.objects.all().delete()
        Product_Member.objects.all().delete()
        User.objects.all().delete()

        call_command("loaddata", "unittests/fixtures/vex_fixtures.json")

        self.maxDiff = None

    @patch("django.utils.timezone.now")
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.vex.services.openvex.user_has_permission_or_403")
    @patch("application.vex.services.openvex.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    def test_openvex_document_product_no_branch(
        self,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        # --- create ---

        parameters = {
            "product": 1,
            "document_id_prefix": "OpenVEX",
            "id_namespace": "https://vex.example.com",
            "author": "Author",
            "role": "Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/create/", parameters, format="json"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_product_no_branch.json", "r"
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(Product.objects.get(id=1), openvex.product)
        self.assertEqual(1, openvex.version)
        self.assertEqual(
            "7feb7c735c24a76887d877709b7ecf0dd4444892e75c1345d7a5b3024f36feac",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("Author", openvex.author)
        self.assertEqual("Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_branches))

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_vulnerabilities))

        # --- update without changes ---

        parameters = {
            "author": "New Author",
            "role": "New Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/update/OpenVEX/2024_0001/",
            parameters,
            format="json",
        )

        self.assertEqual(204, response.status_code)

        # --- update with changes ---

        mock_now.return_value = dateparse.parse_datetime("2020-02-01T04:30:00Z")

        observation_1 = Observation.objects.get(id=1)
        observation_1.description = "new description"
        observation_1.save()

        observation_2 = Observation.objects.get(id=2)
        observation_2.current_status = "Open"
        observation_2.assessment_status = ""
        observation_2.save()

        parameters = {
            "author": "New Author",
            "role": "New Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/update/OpenVEX/2024_0001/",
            parameters,
            format="json",
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0002.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_product_no_branch_update.json", "r"
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(Product.objects.get(id=1), openvex.product)
        self.assertEqual(2, openvex.version)
        self.assertEqual(
            "16c17dda22d8eac14b003b0c4cbce1c8b7b5a3a577720d6430f588a93e48c044",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("New Author", openvex.author)
        self.assertEqual("New Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-02-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_branches))

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.vex.services.openvex.user_has_permission_or_403")
    @patch("application.vex.services.openvex.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    def test_openvex_document_product_branches(
        self,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "product": 2,
            "document_id_prefix": "OpenVEX",
            "id_namespace": "https://vex.example.com",
            "author": "Author",
            "role": "Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/create/", parameters, format="json"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_product_branches.json", "r"
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(Product.objects.get(id=2), openvex.product)
        self.assertEqual(1, openvex.version)
        self.assertEqual(
            "94b35adc77df02b3ce5faf3e0892ca294cc97ac5c469a3f0c619cd47ebec53d8",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("Author", openvex.author)
        self.assertEqual("Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_branches))

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.vex.services.openvex.user_has_permission_or_403")
    @patch("application.vex.services.openvex.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    def test_openvex_document_product_given_branch(
        self,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "product": 2,
            "branch_names": ["main"],
            "document_id_prefix": "OpenVEX",
            "id_namespace": "https://vex.example.com",
            "author": "Author",
            "role": "Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/create/", parameters, format="json"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_product_given_branch.json", "r"
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(Product.objects.get(id=2), openvex.product)
        self.assertEqual(1, openvex.version)
        self.assertEqual(
            "398407e8135486b39c7a14b1100b449fc19c39e76e64152c7ff706efb451582b",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("Author", openvex.author)
        self.assertEqual("Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(1, len(openvex_branches))
        self.assertEqual(2, openvex_branches[0].branch.pk)

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.vex.services.openvex.user_has_permission_or_403")
    @patch("application.vex.services.openvex.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    def test_openvex_document_given_vulnerability(
        self,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "vulnerability_names": ["CVE-vulnerability_2"],
            "document_id_prefix": "OpenVEX",
            "id_namespace": "https://vex.example.com",
            "author": "Author",
            "role": "Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/create/", parameters, format="json"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_given_vulnerability.json", "r"
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(None, openvex.product)
        self.assertEqual(1, openvex.version)
        self.assertEqual(
            "acf86c76016f0c1753dbcdd32bc10f3023ab3d2548380a1cd1c1b58c87b50c1d",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("Author", openvex.author)
        self.assertEqual("Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_branches))

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(1, len(openvex_vulnerabilities))
        self.assertEqual("CVE-vulnerability_2", openvex_vulnerabilities[0].name)

        # --- update without changes ---

        parameters = {
            "author": "New Author",
            "role": "New Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/update/OpenVEX/2024_0001/",
            parameters,
            format="json",
        )

        self.assertEqual(204, response.status_code)

        # --- update with changes ---

        mock_now.return_value = dateparse.parse_datetime("2020-02-01T04:30:00Z")

        observation_2 = Observation.objects.get(id=2)
        observation_2.current_status = "Open"
        observation_2.assessment_status = ""
        observation_2.save()

        parameters = {
            "author": "New Author",
            "role": "New Role",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/openvex_document/update/OpenVEX/2024_0001/",
            parameters,
            format="json",
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=OpenVEX_2024_0001_0002.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/openvex_given_vulnerability_update.json",
            "r",
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        openvex = OpenVEX.objects.get(
            document_id_prefix="OpenVEX", document_base_id="2024_0001"
        )
        self.assertEqual(vex_user, openvex.user)
        self.assertEqual(None, openvex.product)
        self.assertEqual(2, openvex.version)
        self.assertEqual(
            "01c46b464b562c39734cd5d273867e65f9d01f2ac23d370b71679196cf97bc13",
            openvex.content_hash,
        )
        self.assertEqual("https://vex.example.com", openvex.id_namespace)
        self.assertEqual("New Author", openvex.author)
        self.assertEqual("New Role", openvex.role)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            openvex.timestamp,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-02-01T04:30:00Z"),
            openvex.last_updated,
        )

        openvex_branches = OpenVEX_Branch.objects.filter(openvex=openvex)
        self.assertEqual(0, len(openvex_branches))

        openvex_vulnerabilities = OpenVEX_Vulnerability.objects.filter(openvex=openvex)
        self.assertEqual(1, len(openvex_vulnerabilities))
        self.assertEqual("CVE-vulnerability_2", openvex_vulnerabilities[0].name)
