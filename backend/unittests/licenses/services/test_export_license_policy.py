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

        self.license_policy_with_parent = License_Policy(
            name="license_policy_with_parent",
            parent=license_policy,
        )
        self.license_policy_with_parent.save()

        License_Policy_Item(
            license_policy=self.license_policy_with_parent,
            license=License.objects.get(pk=1),
            evaluation_result=License_Policy_Evaluation_Result.RESULT_ALLOWED,
            comment="Permissive license",
        ).save()
        License_Policy_Item(
            license_policy=self.license_policy_with_parent,
            license_expression="MIT OR 3BSD",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_ALLOWED,
            comment="Permissive license expression",
        ).save()
        License_Policy_Item(
            license_policy=self.license_policy_with_parent,
            unknown_license="Unknown",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_ALLOWED,
            comment="Permissive unknown license",
        ).save()
        License_Policy_Item(
            license_policy=self.license_policy_with_parent,
            unknown_license="Another unknown",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
            comment="Forbidden unknown license",
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
            "from_parent": false,
            "license_group": "Permissive Model (Blue Oak Council)",
            "spdx_license": "BlueOak-1.0.0"
        },
        {
            "evaluation_result": "Forbidden",
            "from_parent": false,
            "spdx_license": "0BSD"
        },
        {
            "evaluation_result": "Review required",
            "from_parent": false,
            "license_expression": "MIT OR 3BSD"
        },
        {
            "evaluation_result": "Forbidden",
            "from_parent": false,
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
  from_parent: false
  license_group: Permissive Model (Blue Oak Council)
  spdx_license: BlueOak-1.0.0
- evaluation_result: Forbidden
  from_parent: false
  spdx_license: 0BSD
- evaluation_result: Review required
  from_parent: false
  license_expression: MIT OR 3BSD
- evaluation_result: Forbidden
  from_parent: false
  unknown_license: Unknown
name: public
"""
        self.assertEqual(yaml_data_expected, yaml_data)

    def test_export_json_with_parent(self):
        json_data = export_license_policy_json(self.license_policy_with_parent)

        json_data_expected = """{
    "description": "",
    "items": [
        {
            "evaluation_result": "Allowed",
            "from_parent": true,
            "license_group": "Permissive Model (Blue Oak Council)",
            "spdx_license": "BlueOak-1.0.0"
        },
        {
            "comment": "Permissive license",
            "evaluation_result": "Allowed",
            "from_parent": false,
            "spdx_license": "0BSD"
        },
        {
            "comment": "Permissive license expression",
            "evaluation_result": "Allowed",
            "from_parent": false,
            "license_expression": "MIT OR 3BSD"
        },
        {
            "comment": "Permissive unknown license",
            "evaluation_result": "Allowed",
            "from_parent": false,
            "unknown_license": "Unknown"
        },
        {
            "comment": "Forbidden unknown license",
            "evaluation_result": "Forbidden",
            "from_parent": false,
            "unknown_license": "Another unknown"
        }
    ],
    "name": "license_policy_with_parent",
    "parent": "public"
}"""
        self.assertEqual(json_data_expected, json_data)

    def test_export_yaml_with_parent(self):
        yaml_data = export_license_policy_yaml(self.license_policy_with_parent)

        yaml_data_expected = """description: ''
items:
- evaluation_result: Allowed
  from_parent: true
  license_group: Permissive Model (Blue Oak Council)
  spdx_license: BlueOak-1.0.0
- comment: Permissive license
  evaluation_result: Allowed
  from_parent: false
  spdx_license: 0BSD
- comment: Permissive license expression
  evaluation_result: Allowed
  from_parent: false
  license_expression: MIT OR 3BSD
- comment: Permissive unknown license
  evaluation_result: Allowed
  from_parent: false
  unknown_license: Unknown
- comment: Forbidden unknown license
  evaluation_result: Forbidden
  from_parent: false
  unknown_license: Another unknown
name: license_policy_with_parent
parent: public
"""
        self.assertEqual(yaml_data_expected, yaml_data)
