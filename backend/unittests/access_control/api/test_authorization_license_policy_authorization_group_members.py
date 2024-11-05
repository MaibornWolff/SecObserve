from application.licenses.models import License_Policy
from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationLicensePolicyAuthorizationGroupMembers(TestAuthorizationBase):
    def test_authorization_license_policy_authorization_group_members(self):
        License_Policy.objects.filter(pk__lt=1000).delete()

        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1000, 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 2, 'name': 'oidc_group_2', 'oidc_group': 'oidc_2'}, 'is_manager': False, 'license_policy': 1003, 'authorization_group': 2}, {'id': 1001, 'license_policy_data': {'id': 1004, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 2, 'name': 'oidc_group_2', 'oidc_group': 'oidc_2'}, 'is_manager': True, 'license_policy': 1004, 'authorization_group': 2}, {'id': 1002, 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 3, 'name': 'non_oidc_group', 'oidc_group': ''}, 'is_manager': True, 'license_policy': 1003, 'authorization_group': 3}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/license_policy_authorization_group_members/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1000, 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 2, 'name': 'oidc_group_2', 'oidc_group': 'oidc_2'}, 'is_manager': False, 'license_policy': 1003, 'authorization_group': 2}, {'id': 1001, 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 2, 'name': 'oidc_group_2', 'oidc_group': 'oidc_2'}, 'is_manager': True, 'license_policy': 1004, 'authorization_group': 2}]}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/license_policy_authorization_group_members/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1000, 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 2, 'name': 'oidc_group_2', 'oidc_group': 'oidc_2'}, 'is_manager': False, 'license_policy': 1003, 'authorization_group': 2}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/license_policy_authorization_group_members/1000/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'message': 'No License_Policy_Authorization_Group_Member matches the given query.'}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/license_policy_authorization_group_members/99999/",
                None,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1004,
            "authorization_group": 1,
            "is_manager": False,
        }
        expected_data = "{'id': 1003, 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 1, 'name': 'oidc_group_1', 'oidc_group': 'oidc_1'}, 'is_manager': False, 'license_policy': 1004, 'authorization_group': 1}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_authorization_group_members/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1004,
            "authorization_group": 3,
            "is_manager": False,
        }
        expected_data = "{'message': 'Authorization_Group not found.'}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_authorization_group_members/",
                post_data,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1001,
            "authorization_group": 2,
            "is_manager": False,
        }
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_authorization_group_members/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1003,
            "authorization_group": 1,
            "is_manager": False,
        }
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_authorization_group_members/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1003, 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'authorization_group_data': {'id': 1, 'name': 'oidc_group_1', 'oidc_group': 'oidc_1'}, 'is_manager': True, 'license_policy': 1004, 'authorization_group': 1}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "patch",
                "/api/license_policy_authorization_group_members/1003/",
                {"is_manager": "True"},
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
                "db_product_group_user",
                "patch",
                "/api/license_policy_authorization_group_members/1000/",
                {"is_manager": "True"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_product_group_user",
                "delete",
                "/api/license_policy_authorization_group_members/1003/",
                None,
                204,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_product_group_user",
                "delete",
                "/api/license_policy_authorization_group_members/1000/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )
