from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.access_control.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationLicenseComponentEvidences(TestAuthorizationBase):
    def test_authorization_license_component_evidences_product_member(self):
        self._test_authorization_license_component_evidences()

    def test_authorization_license_component_evidences_product_authorization_group_member(
        self,
    ):
        prepare_authorization_groups()
        self._test_authorization_license_component_evidences()

    def _test_authorization_license_component_evidences(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'product': 1, 'name': 'internal_license_evidence_name', 'evidence': 'internal license evidence', 'license_component': 1}, {'id': 2, 'product': 2, 'name': 'external_license_evidence_name', 'evidence': 'external license evidence', 'license_component': 2}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/license_component_evidences/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'product': 1, 'name': 'internal_license_evidence_name', 'evidence': 'internal license evidence', 'license_component': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_component_evidences/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product': 1, 'name': 'internal_license_evidence_name', 'evidence': 'internal license evidence', 'license_component': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_component_evidences/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No License_Component_Evidence matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_component_evidences/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_component_evidences/99999/",
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
                "/api/license_component_evidences/",
                post_data,
                405,
                None,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/license_component_evidences/1/",
                {"title": "changed"},
                405,
                None,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/license_component_evidences/1/",
                None,
                405,
                None,
            )
        )
