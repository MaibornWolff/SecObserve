from django.core.management import call_command

from application.licenses.models import License, License_Policy, License_Policy_Item
from application.licenses.services.export_license_policy import (
    export_license_policy_json,
    export_license_policy_yaml,
)
from application.licenses.types import License_Policy_Evaluation_Result
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

        license_policy = License_Policy.objects.get(pk=1000)
        license_policy.description = "description_1000"
        license_policy.ignore_component_types = "apk, oci"
        license_policy.save()
        License_Policy_Item(
            license_policy=license_policy,
            license=License.objects.get(pk=1),
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
        ).save()
        License_Policy_Item(
            license_policy=license_policy,
            license_expression="MIT OR 3BSD",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
        ).save()
        License_Policy_Item(
            license_policy=license_policy,
            unknown_license="Unknown",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
        ).save()

        super().setUpClass()

    def test_export_json(self):
        license_policy = License_Policy.objects.get(pk=1000)
        json_data = export_license_policy_json(license_policy)

        json_data_expected = """{
    "description": "description_1000",
    "ignore_component_types": [
        "apk",
        "oci"
    ],
    "items": [
        {
            "evaluation_result": "Allowed",
            "license_group": "Permissive Model (Blue Oak Council)",
            "spdx_license": "BlueOak-1.0.0"
        },
        {
            "evaluation_result": "Forbidden",
            "spdx_license": "0BSD"
        },
        {
            "evaluation_result": "Review required",
            "license_expression": "MIT OR 3BSD"
        },
        {
            "evaluation_result": "Forbidden",
            "unknown_license": "Unknown"
        }
    ],
    "name": "public"
}"""
        self.assertEqual(json_data_expected, json_data)

    def test_export_yaml(self):
        license_policy = License_Policy.objects.get(pk=1000)
        yaml_data = export_license_policy_yaml(license_policy)

        yaml_data_expected = """description: description_1000
ignore_component_types:
- apk
- oci
items:
- evaluation_result: Allowed
  license_group: Permissive Model (Blue Oak Council)
  spdx_license: BlueOak-1.0.0
- evaluation_result: Forbidden
  spdx_license: 0BSD
- evaluation_result: Review required
  license_expression: MIT OR 3BSD
- evaluation_result: Forbidden
  unknown_license: Unknown
name: public
"""
        self.assertEqual(yaml_data_expected, yaml_data)
