from os import path
from unittest.mock import patch
from uuid import UUID

from django.core.management import call_command
from django.test import TestCase
from django.utils import dateparse
from rest_framework.test import APIClient

from application.access_control.models import User
from application.core.models import Observation, Product, Product_Member
from application.licenses.models import License_Component
from application.vex.models import CycloneDX, CycloneDX_Branch, CycloneDX_Vulnerability


class TestCycloneDX(TestCase):
    def setUp(self):
        Observation.objects.all().delete()
        License_Component.objects.all().delete()
        Product.objects.filter(is_product_group=False).delete()
        Product.objects.all().delete()
        Product_Member.objects.all().delete()
        User.objects.all().delete()

        call_command("loaddata", "unittests/fixtures/vex_fixtures.json")

        for observation in Observation.objects.all():
            observation.origin_component_cyclonedx_bom_link = (
                f"urn:cdx:{observation.pk}/{observation.origin_component_name_version}"
            )
            observation.save()

        self.maxDiff = None

    @patch("django.utils.timezone.now")
    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    @patch("application.vex.services.cyclonedx_generator.user_has_permission_or_403")
    @patch("application.vex.services.cyclonedx_generator.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    @patch("cyclonedx.model.bom.uuid4")
    def test_cyclonedx_document_product_no_branch(
        self,
        mock_bom_uuid4,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_bom_uuid4.return_value = UUID("e8d7b87f-83ec-4e41-af84-25f2b1d2739d")
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        # --- create ---

        parameters = {
            "product": 1,
            "document_id_prefix": "CycloneDX",
            "author": "Author",
            "manufacturer": "",
        }

        api_client = APIClient()
        response = api_client.post("/api/vex/cyclonedx_document/create/", parameters, format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(path.dirname(__file__) + "/files/cyclonedx_product_no_branch.json", "r") as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(Product.objects.get(id=1), cyclonedx.product)
        self.assertEqual(1, cyclonedx.version)
        self.assertEqual(
            "47171cd4e4a21045adbf70db1766c3999f99a2256f34d3c2245c76e726de1dae",
            cyclonedx.content_hash,
        )
        self.assertEqual("Author", cyclonedx.author)
        self.assertEqual("", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_branches))

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_vulnerabilities))

        # --- update without changes ---

        parameters = {
            "author": "New Author",
            "manufacturer": "",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/cyclonedx_document/update/CycloneDX/e8d7b87f-83ec-4e41-af84-25f2b1d2739d/",
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
            "author": "",
            "manufacturer": "New manufacturer",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/cyclonedx_document/update/CycloneDX/e8d7b87f-83ec-4e41-af84-25f2b1d2739d/",
            parameters,
            format="json",
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0002.json",
            response.headers["Content-Disposition"],
        )
        with open(path.dirname(__file__) + "/files/cyclonedx_product_no_branch_update.json", "r") as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(Product.objects.get(id=1), cyclonedx.product)
        self.assertEqual(2, cyclonedx.version)
        self.assertEqual(
            "05f17369a5ced1a829b5b09b556ffb95bbe430ff950c1cdbf6f57740e31539e6",
            cyclonedx.content_hash,
        )
        self.assertEqual("", cyclonedx.author)
        self.assertEqual("New manufacturer", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-02-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_branches))

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    @patch("application.vex.services.cyclonedx_generator.user_has_permission_or_403")
    @patch("application.vex.services.cyclonedx_generator.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    @patch("cyclonedx.model.bom.uuid4")
    def test_cyclonedx_document_product_branches(
        self,
        mock_uuid4,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_uuid4.return_value = UUID("e8d7b87f-83ec-4e41-af84-25f2b1d2739d")
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "product": 2,
            "document_id_prefix": "CycloneDX",
            "author": "",
            "manufacturer": "Manufacturer",
        }

        api_client = APIClient()
        response = api_client.post("/api/vex/cyclonedx_document/create/", parameters, format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(path.dirname(__file__) + "/files/cyclonedx_product_branches.json", "r") as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(Product.objects.get(id=2), cyclonedx.product)
        self.assertEqual(1, cyclonedx.version)
        self.assertEqual(
            "f6ace394bcafbd4c857f74a507185d13a37c2d191e006c132979d933263bc43c",
            cyclonedx.content_hash,
        )
        self.assertEqual("", cyclonedx.author)
        self.assertEqual("Manufacturer", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_branches))

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    @patch("application.vex.services.cyclonedx_generator.user_has_permission_or_403")
    @patch("application.vex.services.cyclonedx_generator.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    @patch("cyclonedx.model.bom.uuid4")
    def test_cyclonedx_document_product_given_branch(
        self,
        mock_bom_uuid4,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_bom_uuid4.return_value = UUID("e8d7b87f-83ec-4e41-af84-25f2b1d2739d")
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "product": 2,
            "branches": [2],
            "document_id_prefix": "CycloneDX",
            "author": "",
            "manufacturer": "Manufacturer",
        }

        api_client = APIClient()
        response = api_client.post("/api/vex/cyclonedx_document/create/", parameters, format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(path.dirname(__file__) + "/files/cyclonedx_product_given_branch.json", "r") as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(Product.objects.get(id=2), cyclonedx.product)
        self.assertEqual(1, cyclonedx.version)
        self.assertEqual(
            "44a6d3ef47b4b718c1fa3a5439b16832e794c4b6fc4c1e4af9fbe427a258b36b",
            cyclonedx.content_hash,
        )
        self.assertEqual("", cyclonedx.author)
        self.assertEqual("Manufacturer", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(1, len(cyclonedx_branches))
        self.assertEqual(2, cyclonedx_branches[0].branch.pk)

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_vulnerabilities))

    @patch("django.utils.timezone.now")
    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    @patch("application.vex.services.cyclonedx_generator.user_has_permission_or_403")
    @patch("application.vex.services.cyclonedx_generator.get_current_user")
    @patch("application.core.queries.observation.get_current_user")
    @patch("cyclonedx.model.bom.uuid4")
    def test_cyclonedx_document_given_vulnerability(
        self,
        mock_bom_uuid4,
        mock_get_current_user_1,
        mock_get_current_user_2,
        mock_get_user_has_permission_or_403,
        mock_authenticate,
        mock_now,
    ):
        mock_bom_uuid4.return_value = UUID("e8d7b87f-83ec-4e41-af84-25f2b1d2739d")
        mock_now.return_value = dateparse.parse_datetime("2020-01-01T04:30:00Z")
        vex_user = User.objects.get(username="vex_user")
        mock_authenticate.return_value = vex_user, None
        mock_get_current_user_1.return_value = vex_user
        mock_get_current_user_2.return_value = vex_user

        parameters = {
            "vulnerability_names": ["CVE-vulnerability_2"],
            "document_id_prefix": "CycloneDX",
            "author": "Author",
            "manufacturer": "",
        }

        api_client = APIClient()
        response = api_client.post("/api/vex/cyclonedx_document/create/", parameters, format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0001.json",
            response.headers["Content-Disposition"],
        )
        with open(path.dirname(__file__) + "/files/cyclonedx_given_vulnerability.json", "r") as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(None, cyclonedx.product)
        self.assertEqual(1, cyclonedx.version)
        self.assertEqual(
            "7868880f131bfd05255c9a4bd471818f2e0025ad969e64b4c8f9a325e832c0f7",
            cyclonedx.content_hash,
        )
        self.assertEqual("Author", cyclonedx.author)
        self.assertEqual("", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_branches))

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(1, len(cyclonedx_vulnerabilities))
        self.assertEqual("CVE-vulnerability_2", cyclonedx_vulnerabilities[0].name)

        # --- update without changes ---

        parameters = {
            "author": "New Author",
            "manufacturer": "",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/cyclonedx_document/update/CycloneDX/e8d7b87f-83ec-4e41-af84-25f2b1d2739d/",
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
            "author": "",
            "manufacturer": "Manufacturer",
        }

        api_client = APIClient()
        response = api_client.post(
            "/api/vex/cyclonedx_document/update/CycloneDX/e8d7b87f-83ec-4e41-af84-25f2b1d2739d/",
            parameters,
            format="json",
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(
            "attachment; filename=CycloneDX_e8d7b87f-83ec-4e41-af84-25f2b1d2739d_0002.json",
            response.headers["Content-Disposition"],
        )
        with open(
            path.dirname(__file__) + "/files/cyclonedx_given_vulnerability_update.json",
            "r",
        ) as testfile:
            self.assertEqual(testfile.read(), response._container[0].decode("utf-8"))

        cyclonedx = CycloneDX.objects.get(
            document_id_prefix="CycloneDX", document_base_id="e8d7b87f-83ec-4e41-af84-25f2b1d2739d"
        )
        self.assertEqual(vex_user, cyclonedx.user)
        self.assertEqual(None, cyclonedx.product)
        self.assertEqual(2, cyclonedx.version)
        self.assertEqual(
            "a00b1db24ebf636052927506116feaae0e538b7e3d3f6744a5ecab840e1897ed",
            cyclonedx.content_hash,
        )
        self.assertEqual("", cyclonedx.author)
        self.assertEqual("Manufacturer", cyclonedx.manufacturer)
        self.assertEqual(
            dateparse.parse_datetime("2020-01-01T04:30:00Z"),
            cyclonedx.first_issued,
        )
        self.assertEqual(
            dateparse.parse_datetime("2020-02-01T04:30:00Z"),
            cyclonedx.last_updated,
        )

        cyclonedx_branches = CycloneDX_Branch.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(0, len(cyclonedx_branches))

        cyclonedx_vulnerabilities = CycloneDX_Vulnerability.objects.filter(cyclonedx=cyclonedx)
        self.assertEqual(1, len(cyclonedx_vulnerabilities))
        self.assertEqual("CVE-vulnerability_2", cyclonedx_vulnerabilities[0].name)
