from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.authorization.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationComponents(TestAuthorizationBase):
    def test_authorization_components_product_member(self):
        self._test_authorization_components()

    def test_authorization_components_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_components()

    def _test_authorization_components(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 'e9cf03af3d974272c959020a8716a186', 'product_name': 'db_product_internal', 'product_group_name': 'db_product_group', 'branch_name': '', 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'origin_service_name': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'component_dependencies': '', 'component_cyclonedx_bom_link': '', 'has_observations': False, 'product': 1, 'branch': None, 'origin_service': None}, {'id': 'ebc3f4bcc9e2a8f31860653f7e487cf1', 'product_name': 'db_product_external', 'product_group_name': '', 'branch_name': '', 'component_name_version_type': 'external_component:2.0.0', 'component_purl_namespace': '', 'origin_service_name': '', 'component_name': 'external_component', 'component_version': '2.0.0', 'component_name_version': 'external_component:2.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'component_dependencies': '', 'component_cyclonedx_bom_link': '', 'has_observations': False, 'product': 2, 'branch': None, 'origin_service': None}]}"
        self._test_api(APITest("db_admin", "get", "/api/components/", None, 200, expected_data))

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 'e9cf03af3d974272c959020a8716a186', 'product_name': 'db_product_internal', 'product_group_name': 'db_product_group', 'branch_name': '', 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'origin_service_name': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'component_dependencies': '', 'component_cyclonedx_bom_link': '', 'has_observations': False, 'product': 1, 'branch': None, 'origin_service': None}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/components/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 'e9cf03af3d974272c959020a8716a186', 'product_name': 'db_product_internal', 'product_group_name': 'db_product_group', 'branch_name': '', 'component_name_version_type': 'internal_component:1.0.0', 'component_purl_namespace': '', 'origin_service_name': '', 'component_name': 'internal_component', 'component_version': '1.0.0', 'component_name_version': 'internal_component:1.0.0', 'component_purl': '', 'component_purl_type': '', 'component_cpe': '', 'component_dependencies': '', 'component_cyclonedx_bom_link': '', 'has_observations': False, 'product': 1, 'branch': None, 'origin_service': None}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/components/e9cf03af3d974272c959020a8716a186/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Component matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/components/ebc3f4bcc9e2a8f31860653f7e487cf1/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/components/99999/",
                None,
                404,
                expected_data,
            )
        )
