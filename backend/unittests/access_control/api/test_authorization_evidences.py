from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationEvidences(TestAuthorizationBase):
    def test_authorization_evidences(self):
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
