from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.access_control.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationLicense_Components(TestAuthorizationBase):
    def test_authorization_license_components_product_member(self):
        self._test_authorization_license_components()

    def test_authorization_license_components_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_license_components()

    def _test_authorization_license_components(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'license_data': None, 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'branch_name': '', 'type': 'Non-SPDX', 'title': 'internal license / internal_component:1.0.0', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'upload_filename': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'license_name': 'internal license', 'license_expression': '', 'non_spdx_license': 'internal license', 'evaluation_result': 'Allowed', 'numerical_evaluation_result': 1, 'created': '2022-12-15T17:10:35.513000+01:00', 'import_last_seen': '2022-12-15T17:10:35.513000+01:00', 'last_change': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'branch': None, 'license': None}, {'id': 2, 'license_data': None, 'component_name_version_type': 'external_component:2.0.0', 'component_purl_namespace': '', 'branch_name': '', 'type': 'Non-SPDX', 'title': 'external license / external_component:2.0.0', 'identity_hash': 'bc8e59b7687fe3533616b3914c636389c131eac3bdbda1b67d8d26f890a74007', 'upload_filename': '', 'component_name': 'external_component', 'component_version': '2.0.0', 'component_name_version': 'external_component:2.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'license_name': 'external license', 'license_expression': '', 'non_spdx_license': 'external license', 'evaluation_result': 'Review required', 'numerical_evaluation_result': 2, 'created': '2022-12-15T17:10:35.513000+01:00', 'import_last_seen': '2022-12-15T17:10:35.513000+01:00', 'last_change': '2022-12-15T17:10:35.513000+01:00', 'product': 2, 'branch': None, 'license': None}]}"
        self._test_api(
            APITest(
                "db_admin", "get", "/api/license_components/", None, 200, expected_data
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'license_data': None, 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'branch_name': '', 'type': 'Non-SPDX', 'title': 'internal license / internal_component:1.0.0', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'upload_filename': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'license_name': 'internal license', 'license_expression': '', 'non_spdx_license': 'internal license', 'evaluation_result': 'Allowed', 'numerical_evaluation_result': 1, 'created': '2022-12-15T17:10:35.513000+01:00', 'import_last_seen': '2022-12-15T17:10:35.513000+01:00', 'last_change': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'branch': None, 'license': None}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_components/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'license_data': None, 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'branch_name': '', 'license_policy_name': '', 'license_policy_id': 0, 'evidences': [{'id': 1, 'name': 'internal_license_evidence_name'}], 'type': 'Non-SPDX', 'title': 'internal license / internal_component:1.0.0', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'upload_filename': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'component_dependencies': '', 'license_name': 'internal license', 'license_expression': '', 'non_spdx_license': 'internal license', 'evaluation_result': 'Allowed', 'numerical_evaluation_result': 1, 'created': '2022-12-15T17:10:35.513000+01:00', 'import_last_seen': '2022-12-15T17:10:35.513000+01:00', 'last_change': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'branch': None, 'license': None}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_components/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No License_Component matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_components/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_components/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"product": 1}
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_components/",
                post_data,
                405,
                None,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/license_components/1/",
                {"title": "changed"},
                405,
                None,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/license_components/1/",
                None,
                405,
                None,
            )
        )
