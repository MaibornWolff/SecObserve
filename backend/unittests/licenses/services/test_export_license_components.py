from datetime import datetime

from django.core.management import call_command

from application.core.models import Product
from application.licenses.services.export_license_components import (
    export_license_components_excel,
)
from unittests.base_test_case import BaseTestCase


class TestLicenseGroupMemberSerializer(BaseTestCase):
    @classmethod
    def setUpClass(self):
        call_command(
            "loaddata",
            [
                "application/licenses/fixtures/initial_data.json",
                "unittests/fixtures/unittests_fixtures.json",
                "unittests/fixtures/unittests_license_fixtures.json",
            ],
        )

        super().setUpClass()

    def test_export_license_components_excel(self):
        product = Product.objects.get(pk=1)

        workbook = export_license_components_excel(product)
        worksheet = workbook["License Components"]

        i = 0
        for row in worksheet.rows:
            i += 1
            self.assertEqual(24, len(row))
        self.assertEqual(2, i)

        actual_values = []
        for row in worksheet.values:
            for value in row:
                actual_values.append(value)
        expected_values = [
            "Branch",
            "Branch id",
            "Component cpe",
            "Component dependencies",
            "Component name",
            "Component name version",
            "Component purl",
            "Component purl type",
            "Component version",
            "Created",
            "Evaluation result",
            "Id",
            "Import last seen",
            "Last change",
            "License",
            "License expression",
            "License id",
            "License name",
            "Multiple licenses",
            "Non spdx license",
            "Numerical evaluation result",
            "Product",
            "Product id",
            "Upload filename",
            None,
            None,
            "",
            "",
            "internal_component",
            "internal_component:1.0.0",
            "",
            "",
            "1.0.0",
            datetime(2022, 12, 15, 16, 10, 35, 513000),
            "Allowed",
            1,
            datetime(2022, 12, 15, 16, 10, 35, 513000),
            datetime(2022, 12, 15, 16, 10, 35, 513000),
            None,
            "",
            None,
            "internal license",
            "",
            "internal license",
            1,
            "db_product_internal",
            1,
            "",
        ]
        self.assertEqual(expected_values, actual_values)
