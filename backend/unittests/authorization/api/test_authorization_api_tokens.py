from application.access_control.models import API_Token, User
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

        db_internal_write = User.objects.get(username="db_internal_write")
        API_Token(user=db_internal_write, api_token_hash="hash").save()

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 2, 'name': 'db_internal_write', 'product': None, 'product_group': None}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_tokens/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'count': 0, 'next': None, 'previous': None, 'results': []}"
        self._test_api(
            APITest(
                "db_internal_read",
                "get",
                "/api/api_tokens/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )
