from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.authorization.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationProductMembers(TestAuthorizationBase):
    def test_authorization_product_authorization_group_members(self):
        prepare_authorization_groups()

        expected_data = "{'count': 4, 'next': None, 'previous': None, 'results': [{'id': 1, 'authorization_group_data': {'id': 4, 'name': 'db_group_internal_write', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 5, 'product': 1, 'authorization_group': 4}, {'id': 2, 'authorization_group_data': {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 1, 'product': 1, 'authorization_group': 5}, {'id': 3, 'authorization_group_data': {'id': 6, 'name': 'db_group_external', 'oidc_group': ''}, 'product_data': {'id': 2, 'name': 'db_product_external', 'is_product_group': False}, 'role': 5, 'product': 2, 'authorization_group': 6}, {'id': 4, 'authorization_group_data': {'id': 7, 'name': 'db_group_product_group', 'oidc_group': ''}, 'product_data': {'id': 3, 'name': 'db_product_group', 'is_product_group': True}, 'role': 5, 'product': 3, 'authorization_group': 7}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/product_authorization_group_members/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'authorization_group_data': {'id': 4, 'name': 'db_group_internal_write', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 5, 'product': 1, 'authorization_group': 4}, {'id': 2, 'authorization_group_data': {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 1, 'product': 1, 'authorization_group': 5}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_authorization_group_members/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1, 'authorization_group_data': {'id': 4, 'name': 'db_group_internal_write', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 5, 'product': 1, 'authorization_group': 4}, {'id': 2, 'authorization_group_data': {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 1, 'product': 1, 'authorization_group': 5}, {'id': 4, 'authorization_group_data': {'id': 7, 'name': 'db_group_product_group', 'oidc_group': ''}, 'product_data': {'id': 3, 'name': 'db_product_group', 'is_product_group': True}, 'role': 5, 'product': 3, 'authorization_group': 7}]}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/product_authorization_group_members/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'authorization_group_data': {'id': 4, 'name': 'db_group_internal_write', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 5, 'product': 1, 'authorization_group': 4}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_authorization_group_members/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No Product_Authorization_Group_Member matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_authorization_group_members/3/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_authorization_group_members/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"role": 3, "product": 1, "authorization_group": 8}
        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/product_authorization_group_members/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 5, 'authorization_group_data': {'id': 8, 'name': 'db_group_unused', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 3, 'product': 1, 'authorization_group': 8}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/product_authorization_group_members/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"role": 2}
        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/product_authorization_group_members/2/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 2, 'authorization_group_data': {'id': 5, 'name': 'db_group_internal_read', 'oidc_group': ''}, 'product_data': {'id': 1, 'name': 'db_product_internal', 'is_product_group': False}, 'role': 2, 'product': 1, 'authorization_group': 5}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/product_authorization_group_members/2/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/product_authorization_group_members/2/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/product_authorization_group_members/2/",
                None,
                204,
                expected_data,
            )
        )
