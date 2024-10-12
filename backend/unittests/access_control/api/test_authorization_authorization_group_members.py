from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationAuthorizationGroupMembers(TestAuthorizationBase):
    def test_authorization_authorization_group_members(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 2, 'username': 'db_internal_write', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_write', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-07T20:24:53+01:00', 'has_password': False}, 'is_manager': True, 'authorization_group': 3, 'user': 2}, {'id': 2, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 3, 'username': 'db_internal_read', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_read', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-07T20:25:06+01:00', 'has_password': False}, 'is_manager': False, 'authorization_group': 3, 'user': 3}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/authorization_group_members/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 2, 'username': 'db_internal_write', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_write', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-07T20:24:53+01:00', 'has_password': False}, 'is_manager': True, 'authorization_group': 3, 'user': 2}, {'id': 2, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 3, 'username': 'db_internal_read', 'full_name': 'db_internal_read'}, 'is_manager': False, 'authorization_group': 3, 'user': 3}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_group_members/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'count': 0, 'next': None, 'previous': None, 'results': []}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/authorization_group_members/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )
        expected_data = "{'id': 1, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 2, 'username': 'db_internal_write', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_write', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'setting_list_size': 'medium', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>], 'setting_list_properties': '', 'oidc_groups_hash': '', 'is_oidc_user': False, 'date_joined': '2022-12-07T20:24:53+01:00', 'has_password': False}, 'is_manager': True, 'authorization_group': 3, 'user': 2}"
        self._test_api(
            APITest(
                username="db_internal_write",
                method="get",
                url="/api/authorization_group_members/1/",
                post_data=None,
                expected_status_code=200,
                expected_data=expected_data,
                no_second_user=True,
            )
        )

        expected_data = (
            "{'message': 'No Authorization_Group_Member matches the given query.'}"
        )
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/authorization_group_members/1/",
                None,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/authorization_group_members/99999/",
                None,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"authorization_group": 3, "user": 1, "is_manager": False}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/authorization_group_members/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )
        expected_data = "{'id': 3, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 1, 'username': 'db_admin', 'full_name': 'db_admin'}, 'is_manager': False, 'authorization_group': 3, 'user': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/authorization_group_members/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"is_manager": True}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/authorization_group_members/3/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 3, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'user_data': {'id': 1, 'username': 'db_admin', 'full_name': 'db_admin'}, 'is_manager': True, 'authorization_group': 3, 'user': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/authorization_group_members/3/",
                post_data,
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
                "db_internal_read",
                "delete",
                "/api/authorization_group_members/3/",
                None,
                403,
                expected_data,
                no_second_user=True,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/authorization_group_members/3/",
                None,
                204,
                expected_data,
                no_second_user=True,
            )
        )
