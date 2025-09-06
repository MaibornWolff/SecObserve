from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.authorization.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationConcluded(TestAuthorizationBase):
    def test_authorization_concluded_licenses_product_member(self):
        self._test_authorization_concluded_licenses()

    def test_authorization_concluded_licenses_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_concluded_licenses()

    def _test_authorization_concluded_licenses(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'user_data': {'id': 1, 'username': 'db_admin', 'first_name': '', 'last_name': '', 'full_name': 'db_admin', 'email': '', 'is_active': True, 'is_superuser': True, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'setting_package_info_preference': 'open/source/insights', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-04T11:09:18.495000+01:00', 'has_password': True}, 'component_name_version': 'internal_component:1.0.0 (npm)', 'manual_concluded_spdx_license_id': '', 'component_purl_type': 'npm', 'component_name': 'internal_component', 'component_version': '1.0.0', 'manual_concluded_license_expression': 'expression', 'manual_concluded_non_spdx_license': '', 'last_updated': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'manual_concluded_spdx_license': None, 'user': 1}, {'id': 2, 'product_data': {'id': 2, 'name': 'db_product_external', 'is_product_group': False}, 'user_data': {'id': 1, 'username': 'db_admin', 'first_name': '', 'last_name': '', 'full_name': 'db_admin', 'email': '', 'is_active': True, 'is_superuser': True, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'setting_package_info_preference': 'open/source/insights', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-04T11:09:18.495000+01:00', 'has_password': True}, 'component_name_version': 'external_component:2.0.0 (pypi)', 'manual_concluded_spdx_license_id': '', 'component_purl_type': 'pypi', 'component_name': 'external_component', 'component_version': '2.0.0', 'manual_concluded_license_expression': '', 'manual_concluded_non_spdx_license': 'non spdx', 'last_updated': '2022-12-15T17:10:35.513000+01:00', 'product': 2, 'manual_concluded_spdx_license': None, 'user': 1}]}"
        self._test_api(APITest("db_admin", "get", "/api/concluded_licenses/", None, 200, expected_data))

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'user_data': {'id': 1, 'username': 'db_admin', 'full_name': 'db_admin'}, 'component_name_version': 'internal_component:1.0.0 (npm)', 'manual_concluded_spdx_license_id': '', 'component_purl_type': 'npm', 'component_name': 'internal_component', 'component_version': '1.0.0', 'manual_concluded_license_expression': 'expression', 'manual_concluded_non_spdx_license': '', 'last_updated': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'manual_concluded_spdx_license': None, 'user': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/concluded_licenses/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'user_data': {'id': 1, 'username': 'db_admin', 'full_name': 'db_admin'}, 'component_name_version': 'internal_component:1.0.0 (npm)', 'manual_concluded_spdx_license_id': '', 'component_purl_type': 'npm', 'component_name': 'internal_component', 'component_version': '1.0.0', 'manual_concluded_license_expression': 'expression', 'manual_concluded_non_spdx_license': '', 'last_updated': '2022-12-15T17:10:35.513000+01:00', 'product': 1, 'manual_concluded_spdx_license': None, 'user': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/concluded_licenses/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Concluded_License matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/concluded_licenses/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/concluded_licenses/99999/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/concluded_licenses/1/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/concluded_licenses/1/",
                None,
                204,
                None,
                no_second_user=True,
            )
        )
