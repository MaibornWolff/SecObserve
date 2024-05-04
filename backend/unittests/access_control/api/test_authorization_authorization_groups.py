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

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 4, 'name': 'db_group_internal_write', 'oidc_group': '', 'users': [2]}]}"
        expected_data_product_group = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 7, 'name': 'db_group_product_group', 'oidc_group': '', 'users': [6]}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_groups/",
                None,
                200,
                expected_data,
                expected_data_product_group=expected_data_product_group,
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
                no_second_user=True,
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

        expected_data = "{'id': 9, 'name': 'string', 'oidc_group': 'oidc', 'users': []}"
        self._test_api(
            APITest(
                "db_admin",
                "post",
                "/api/authorization_groups/",
                {
                    "name": "string",
                    "oidc_group": "oidc",
                },
                201,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/authorization_groups/",
                {
                    "name": "string",
                    "oidc_group": "oidc",
                },
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = (
            "{'id': 9, 'name': 'changed_string', 'oidc_group': 'oidc', 'users': []}"
        )
        self._test_api(
            APITest(
                "db_admin",
                "patch",
                "/api/authorization_groups/9/",
                {"name": "changed_string"},
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/authorization_groups/9/",
                {"name": "changed_string"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/authorization_groups/9/",
                None,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"user": 2}

        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/authorization_groups/9/add_user/",
                post_data,
                403,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_admin",
                "post",
                "/api/authorization_groups/9/add_user/",
                post_data,
                204,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/authorization_groups/9/remove_user/",
                post_data,
                403,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_admin",
                "post",
                "/api/authorization_groups/9/remove_user/",
                post_data,
                204,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_admin",
                "delete",
                "/api/authorization_groups/9/",
                None,
                204,
                None,
                no_second_user=True,
            )
        )
