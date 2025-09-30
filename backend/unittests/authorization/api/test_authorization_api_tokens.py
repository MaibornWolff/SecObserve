from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationApiTokens(TestAuthorizationBase):
    def test_authorization_api_tokens(self):
        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 5, 'name': '-product-2-api_token-', 'product': 2, 'product_group': None}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/api_tokens/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_tokens/",
                None,
                403,
                expected_data,
                no_second_user=True,
            )
        )
