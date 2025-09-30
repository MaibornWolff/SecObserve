from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.authorization.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationEvidences(TestAuthorizationBase):
    def test_authorization_evidences_product_member(self):
        self._test_authorization_evidences()

    def test_authorization_evidences_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_evidences()

    def _test_authorization_evidences(self):
        expected_data = "{'id': 1, 'product': 1, 'name': 'db_evidence_internal', 'evidence': 'abc', 'observation': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Evidence matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/99999/",
                None,
                404,
                expected_data,
            )
        )
