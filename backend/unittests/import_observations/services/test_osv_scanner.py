from datetime import datetime, timezone
from json import loads
from unittest.mock import call, patch

from django.core.management import call_command

from application.core.models import Branch, Product
from application.import_observations.models import Parser
from application.import_observations.parsers.osv.parser import (
    OSV_Component,
    OSV_Vulnerability,
)
from application.import_observations.services.import_observations import (
    ImportParameters,
)
from application.import_observations.services.osv_scanner import (
    scan_branch,
    scan_license_components,
    scan_product,
)
from application.licenses.models import License_Component
from unittests.base_test_case import BaseTestCase


class MockResponse:
    def __init__(self, filename):
        self.filename = filename

    def raise_for_status(self):
        pass

    def json(self):
        with open(
            f"unittests/import_observations/services/files/{self.filename}"
        ) as file:
            return loads(file.read())


class TestImportObservations(BaseTestCase):
    def setUp(self):
        call_command(
            "loaddata",
            [
                "application/licenses/fixtures/initial_data.json",
                "unittests/fixtures/unittests_fixtures.json",
                "unittests/fixtures/unittests_license_fixtures.json",
            ],
        )
        Parser.objects.create(
            name="OSV (Open Source Vulnerabilities)", type="SCA", source="Other"
        )

    @patch("application.import_observations.services.osv_scanner.scan_branch")
    @patch(
        "application.import_observations.services.osv_scanner.get_license_components_no_branch"
    )
    @patch(
        "application.import_observations.services.osv_scanner.scan_license_components"
    )
    def test_scan_product_no_branch(
        self,
        mock_scan_license_components,
        mock_get_license_components_no_branch,
        mock_scan_branch,
    ):
        product = Product.objects.get(id=1)
        Branch.objects.filter(product=product).delete()
        license_components = list(License_Component.objects.all())
        mock_scan_license_components.return_value = (4, 5, 6)
        mock_get_license_components_no_branch.return_value = license_components

        numbers = scan_product(product)

        self.assertEqual((4, 5, 6), numbers)
        mock_scan_branch.assert_not_called()
        mock_get_license_components_no_branch.assert_called_with(product)
        mock_scan_license_components.assert_called_with(
            license_components, product, None
        )

    @patch("application.import_observations.services.osv_scanner.scan_branch")
    @patch(
        "application.import_observations.services.osv_scanner.get_license_components_no_branch"
    )
    @patch(
        "application.import_observations.services.osv_scanner.scan_license_components"
    )
    def test_scan_product_with_branches(
        self,
        mock_scan_license_components,
        mock_get_license_components_no_branch,
        mock_scan_branch,
    ):
        product = Product.objects.get(id=1)
        branches = list(Branch.objects.filter(product=product))
        license_components = list(License_Component.objects.all())
        mock_scan_branch.return_value = (1, 2, 3)
        mock_scan_license_components.return_value = (4, 5, 6)
        mock_get_license_components_no_branch.return_value = license_components

        numbers = scan_product(product)

        self.assertEqual((6, 9, 12), numbers)
        mock_scan_branch.assert_has_calls([call(branches[0]), call(branches[1])])
        mock_get_license_components_no_branch.assert_called_with(product)
        mock_scan_license_components.assert_called_with(
            license_components, product, None
        )

    @patch(
        "application.import_observations.services.osv_scanner.get_license_components_for_branch"
    )
    @patch(
        "application.import_observations.services.osv_scanner.scan_license_components"
    )
    def test_scan_branch(
        self, mock_scan_license_components, mock_get_license_components_for_branch
    ):
        product = Product.objects.get(id=1)
        branch = Branch.objects.filter(product=product).first()
        license_components = list(License_Component.objects.all())
        mock_scan_license_components.return_value = (4, 5, 6)
        mock_get_license_components_for_branch.return_value = license_components

        numbers = scan_branch(branch)

        self.assertEqual((4, 5, 6), numbers)
        mock_get_license_components_for_branch.assert_called_with(branch)
        mock_scan_license_components.assert_called_with(
            license_components, product, branch
        )

    @patch("requests.post")
    @patch(
        "application.import_observations.services.osv_scanner.OSVParser.get_observations"
    )
    @patch("application.import_observations.services.osv_scanner._process_data")
    def test_scan_license_components_no_license_components(
        self, mock_process_data, mock_get_observations, mock_requests_post
    ):
        product = Product.objects.get(id=1)

        numbers = scan_license_components([], product, None)

        self.assertEqual((0, 0, 0), numbers)
        mock_requests_post.assert_not_called()
        mock_get_observations.assert_not_called()
        mock_process_data.assert_not_called()

    @patch("requests.post")
    @patch(
        "application.import_observations.services.osv_scanner.OSVParser.get_observations"
    )
    @patch("application.import_observations.services.osv_scanner._process_data")
    @patch(
        "application.import_observations.services.osv_scanner.Vulnerability_Check.objects.update_or_create"
    )
    def test_scan_license_components_error_length(
        self,
        mock_vulnerability_check,
        mock_process_data,
        mock_get_observations,
        mock_requests_post,
    ):
        license_components: list[License_Component] = list(
            License_Component.objects.all()
        )
        license_components[0].component_purl = "pkg:pypi/django@4.2.11"
        license_components[1].component_purl = (
            "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"
        )
        product = Product.objects.get(id=1)
        branch = Branch.objects.get(id=1)

        response = MockResponse("osv_querybatch_error_length.json")
        mock_requests_post.return_value = response

        with self.assertRaises(Exception) as e:
            scan_license_components(license_components, product, branch)

        self.assertEqual(
            "Number of results is different than number of components",
            str(e.exception),
        )

        mock_requests_post.assert_called_with(
            url="https://api.osv.dev/v1/querybatch",
            data='{"queries": [{"package": {"purl": "pkg:pypi/django@4.2.11"}}, {"package": {"purl": "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"}}]}',
            timeout=300,
        )

        mock_get_observations.assert_not_called()
        mock_process_data.assert_not_called()
        mock_vulnerability_check.assert_not_called()

    @patch("requests.post")
    @patch(
        "application.import_observations.services.osv_scanner.OSVParser.get_observations"
    )
    @patch("application.import_observations.services.osv_scanner._process_data")
    @patch(
        "application.import_observations.services.osv_scanner.Vulnerability_Check.objects.update_or_create"
    )
    def test_scan_license_components_error_next_page_token(
        self,
        mock_vulnerability_check,
        mock_process_data,
        mock_get_observations,
        mock_requests_post,
    ):
        license_components: list[License_Component] = list(
            License_Component.objects.all()
        )
        license_components[0].component_purl = "pkg:pypi/django@4.2.11"
        license_components[1].component_purl = (
            "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"
        )
        product = Product.objects.get(id=1)
        branch = Branch.objects.get(id=1)

        response = MockResponse("osv_querybatch_error_next_page_token.json")
        mock_requests_post.return_value = response

        with self.assertRaises(Exception) as e:
            scan_license_components(license_components, product, branch)

        self.assertEqual(
            "Next page token is not yet supported",
            str(e.exception),
        )

        mock_requests_post.assert_called_with(
            url="https://api.osv.dev/v1/querybatch",
            data='{"queries": [{"package": {"purl": "pkg:pypi/django@4.2.11"}}, {"package": {"purl": "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"}}]}',
            timeout=300,
        )

        mock_get_observations.assert_not_called()
        mock_process_data.assert_not_called()
        mock_vulnerability_check.assert_not_called()

    @patch("requests.post")
    @patch(
        "application.import_observations.services.osv_scanner.OSVParser.get_observations"
    )
    @patch("application.import_observations.services.osv_scanner._process_data")
    @patch(
        "application.import_observations.services.osv_scanner.Vulnerability_Check.objects.update_or_create"
    )
    def test_scan_license_components_success(
        self,
        mock_vulnerability_check,
        mock_process_data,
        mock_get_observations,
        mock_requests_post,
    ):
        license_components: list[License_Component] = list(
            License_Component.objects.all()
        )
        license_components[0].component_purl = "pkg:pypi/django@4.2.11"
        license_components[1].component_purl = (
            "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"
        )
        product = Product.objects.get(id=1)
        branch = Branch.objects.get(id=1)

        response = MockResponse("osv_querybatch_success.json")
        mock_requests_post.return_value = response
        mock_process_data.return_value = (1, 2, 3, "OSV (Open Source Vulnerabilities)")

        numbers = scan_license_components(license_components, product, branch)

        self.assertEqual((1, 2, 3), numbers)
        mock_requests_post.assert_called_with(
            url="https://api.osv.dev/v1/querybatch",
            data='{"queries": [{"package": {"purl": "pkg:pypi/django@4.2.11"}}, {"package": {"purl": "pkg:golang/golang.org/x/net@v0.25.1-0.20240603202750-6249541f2a6c"}}]}',
            timeout=300,
        )

        osv_components = [
            OSV_Component(
                license_component=license_components[0],
                vulnerabilities={
                    OSV_Vulnerability(
                        id="GHSA-795c-9xpc-xw6g",
                        modified=datetime(2024, 8, 7, 20, 1, 58, 452618, timezone.utc),
                    ),
                    OSV_Vulnerability(
                        id="GHSA-5hgc-2vfp-mqvc",
                        modified=datetime(
                            2024, 10, 30, 19, 23, 43, 662562, timezone.utc
                        ),
                    ),
                },
            ),
            OSV_Component(
                license_component=license_components[1],
                vulnerabilities={
                    OSV_Vulnerability(
                        id="GO-2024-3333",
                        modified=datetime(2024, 12, 20, 20, 37, 27, 0, timezone.utc),
                    ),
                },
            ),
        ]

        mock_get_observations.assert_called_with(osv_components, product, branch)
        mock_process_data.assert_called_with(
            ImportParameters(
                product=product,
                branch=branch,
                parser=Parser.objects.get(name="OSV (Open Source Vulnerabilities)"),
                filename="",
                api_configuration_name="",
                service="",
                docker_image_name_tag="",
                endpoint_url="",
                kubernetes_cluster="",
                imported_observations=mock_get_observations.return_value,
            )
        )
        mock_vulnerability_check.assert_called_with(
            product=product,
            branch=branch,
            filename="",
            api_configuration_name="",
            defaults={
                "last_import_observations_new": 1,
                "last_import_observations_updated": 2,
                "last_import_observations_resolved": 3,
                "scanner": "OSV (Open Source Vulnerabilities)",
            },
        )
