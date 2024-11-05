from application.licenses.models import License_Policy
from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationLicensePolicyItems(TestAuthorizationBase):
    def test_authorization_license_policy_items(self):
        License_Policy.objects.filter(pk__lt=1000).delete()

        expected_data = "{'count': 5, 'next': None, 'previous': None, 'results': [{'id': 1000, 'license_spdx_id': '', 'license_group_name': 'Permissive Model (Blue Oak Council)', 'license_policy_data': {'id': 1000, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': False, 'name': 'public', 'description': '', 'is_public': True, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Allowed', 'license_policy': 1000, 'license_group': 1, 'license': None}, {'id': 1001, 'license_spdx_id': '0BSD', 'license_group_name': '', 'license_policy_data': {'id': 1001, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_read_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Forbidden', 'license_policy': 1001, 'license_group': None, 'license': 1}, {'id': 1002, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1002, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Two unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1002, 'license_group': None, 'license': None}, {'id': 1003, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Three unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1003, 'license_group': None, 'license': None}, {'id': 1004, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1004, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Four unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1004, 'license_group': None, 'license': None}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/license_policy_items/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1000, 'license_spdx_id': '', 'license_group_name': 'Permissive Model (Blue Oak Council)', 'license_policy_data': {'id': 1000, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': False, 'name': 'public', 'description': '', 'is_public': True, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Allowed', 'license_policy': 1000, 'license_group': 1, 'license': None}, {'id': 1002, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1002, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Two unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1002, 'license_group': None, 'license': None}, {'id': 1003, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1003, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Three unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1003, 'license_group': None, 'license': None}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policy_items/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1000, 'license_spdx_id': '', 'license_group_name': 'Permissive Model (Blue Oak Council)', 'license_policy_data': {'id': 1000, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': False, 'name': 'public', 'description': '', 'is_public': True, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Allowed', 'license_policy': 1000, 'license_group': 1, 'license': None}, {'id': 1003, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1003, 'is_manager': False, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_not_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Three unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1003, 'license_group': None, 'license': None}, {'id': 1004, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Four unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1004, 'license_group': None, 'license': None}]}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "get",
                "/api/license_policy_items/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1002, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1002, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Two unknown licenses', 'evaluation_result': 'Unknown', 'license_policy': 1002, 'license_group': None, 'license': None}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policy_items/1002/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )
        expected_data = "{'message': 'No License_Policy_Item matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policy_items/1001/",
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
                "/api/license_policy_items/99999/",
                None,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1002,
            "license_group": 2,
            "unknown_license": "",
            "evaluation_result": "Allowed",
        }
        expected_data = "{'id': 1005, 'license_spdx_id': '', 'license_group_name': 'Permissive Gold (Blue Oak Council)', 'license_policy_data': {'id': 1002, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Allowed', 'license_policy': 1002, 'license_group': 2, 'license': None}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_policy_items/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1000,
            "license_group": 2,
            "unknown_license": "",
            "evaluation_result": "Allowed",
        }
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_policy_items/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1004,
            "license_group": 2,
            "unknown_license": "",
            "evaluation_result": "Allowed",
        }
        expected_data = "{'id': 1006, 'license_spdx_id': '', 'license_group_name': 'Permissive Gold (Blue Oak Council)', 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': '', 'evaluation_result': 'Allowed', 'license_policy': 1004, 'license_group': 2, 'license': None}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_items/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1003,
            "license_group": 2,
            "unknown_license": "",
            "evaluation_result": "Allowed",
        }
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_product_group_user",
                "post",
                "/api/license_policy_items/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {
            "license_policy": 1001,
            "license_group": 2,
            "unknown_license": "",
            "evaluation_result": "Allowed",
        }
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/license_policy_items/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1002, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1002, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': True, 'has_authorization_groups': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Two unknown licenses', 'evaluation_result': 'Review required', 'license_policy': 1002, 'license_group': None, 'license': None}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/license_policy_items/1002/",
                {
                    "unknown_license": "Two unknown licenses",
                    "evaluation_result": "Review required",
                },
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
                "patch",
                "/api/license_policy_items/1001/",
                {"is_manager": "True"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1004, 'license_spdx_id': '', 'license_group_name': '', 'license_policy_data': {'id': 1004, 'is_manager': True, 'has_products': False, 'has_items': True, 'has_users': False, 'has_authorization_groups': True, 'name': 'authorization_group_manager', 'description': '', 'is_public': False, 'ignore_component_types': ''}, 'unknown_license': 'Four unknown licenses', 'evaluation_result': 'Review required', 'license_policy': 1004, 'license_group': None, 'license': None}"
        self._test_api(
            APITest(
                "db_product_group_user",
                "patch",
                "/api/license_policy_items/1004/",
                {
                    "unknown_license": "Four unknown licenses",
                    "evaluation_result": "Review required",
                },
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
                "/api/license_policy_items/1003/",
                {"is_manager": "True"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/license_policy_items/1002/",
                None,
                204,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/license_policy_items/1001/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_product_group_user",
                "delete",
                "/api/license_policy_items/1004/",
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
                "/api/license_policy_items/1003/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )
