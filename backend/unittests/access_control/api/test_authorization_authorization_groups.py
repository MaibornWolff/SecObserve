from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.access_control.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationAuthorizationGroups(TestAuthorizationBase):
    def test_authorization_authorization_groups(self):
        prepare_authorization_groups()

        expected_data = "{'count': 5, 'next': None, 'previous': None, 'results': [{'id': 4, 'name': 'db_group_internal_write', 'oidc_group': '', 'users': [2]}, {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': '', 'users': [3]}, {'id': 6, 'name': 'db_group_external', 'oidc_group': '', 'users': [4]}, {'id': 7, 'name': 'db_group_product_group', 'oidc_group': '', 'users': [6]}, {'id': 8, 'name': 'db_group_unused', 'oidc_group': '', 'users': []}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/authorization_groups/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 5, 'next': None, 'previous': None, 'results': [{'id': 4, 'name': 'db_group_internal_write', 'oidc_group': '', 'users': [2]}, {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': '', 'users': [3]}, {'id': 6, 'name': 'db_group_external', 'oidc_group': '', 'users': [4]}, {'id': 7, 'name': 'db_group_product_group', 'oidc_group': '', 'users': [6]}, {'id': 8, 'name': 'db_group_unused', 'oidc_group': '', 'users': []}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_groups/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 4, 'name': 'db_group_internal_write', 'oidc_group': '', 'users': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_groups/4/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Authorization_Group matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_groups/99999/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 6, 'name': 'db_group_external', 'oidc_group': '', 'users': [4]}]}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/authorization_groups/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = (
            "{'id': 6, 'name': 'db_group_external', 'oidc_group': '', 'users': [4]}"
        )
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/authorization_groups/6/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Authorization_Group matches the given query.'}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/authorization_groups/4/",
                None,
                404,
                expected_data,
            )
        )
