from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationProductApiTokens(TestAuthorizationBase):
    def test_authorization_product_api_tokens(self):
        expected_data = "{'results': [{'id': 2, 'role': 2}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/product_api_tokens/?product=2",
                None,
                200,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_api_tokens/?product=2",
                None,
                403,
                None,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_external",
                "post",
                "/api/product_api_tokens/",
                {"id": 1, "role": 2},
                403,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/product_api_tokens/",
                {"id": 1, "role": 2},
                201,
                None,
            )
        )

        expected_data = "{'results': [{'id': 1, 'role': 2}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_api_tokens/?product=1",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_external",
                "delete",
                "/api/product_api_tokens/1/",
                None,
                403,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/product_api_tokens/1/",
                None,
                204,
                None,
            )
        )
