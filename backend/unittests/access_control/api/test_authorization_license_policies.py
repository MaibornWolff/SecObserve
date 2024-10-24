from application.licenses.models import License_Policy
from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationLicensePolicies(TestAuthorizationBase):
    def test_authorization_license_policies(self):
        License_Policy.objects.filter(pk__lt=1000).delete()

        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1000, 'is_manager': False, 'has_products': False, 'name': 'public', 'description': '', 'is_public': True, 'users': []}, {'id': 1001, 'is_manager': False, 'has_products': False, 'name': 'internal_read_not_manager', 'description': '', 'is_public': False, 'users': [3, 4]}, {'id': 1002, 'is_manager': False, 'has_products': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'users': [2]}]}"
        self._test_api(
            APITest(
                "db_admin", "get", "/api/license_policies/", None, 200, expected_data
            )
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1000, 'is_manager': False, 'has_products': False, 'name': 'public', 'description': '', 'is_public': True, 'users': []}, {'id': 1002, 'is_manager': True, 'has_products': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'users': [2]}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policies/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1002, 'is_manager': True, 'has_products': False, 'name': 'internal_write_manager', 'description': '', 'is_public': False, 'users': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policies/1002/",
                None,
                200,
                expected_data,
                no_second_user=True,
            )
        )
        expected_data = "{'message': 'No License_Policy matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/license_policies/1001/",
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
                "/api/license_policies/99999/",
                None,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"name": "new_license_policy"}
        expected_data = "{'id': 1003, 'is_manager': True, 'has_products': False, 'name': 'new_license_policy', 'description': '', 'is_public': False, 'users': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_policies/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"name": "new_license_policy_external"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_external",
                "post",
                "/api/license_policies/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'id': 1002, 'is_manager': True, 'has_products': False, 'name': 'internal_write_manager', 'description': 'changed', 'is_public': False, 'users': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/license_policies/1002/",
                {"description": "changed"},
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
                "/api/license_policies/1000/",
                {"description": "changed"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/license_policies/1001/",
                {"description": "changed"},
                403,
                expected_data,
                no_second_user=True,
            )
        )

        post_data = {"name": "copied_license_policy"}
        expected_data = "{'id': 1004, 'is_manager': True, 'has_products': False, 'name': 'copied_license_policy', 'description': 'changed', 'is_public': False, 'users': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_policies/1002/copy/",
                post_data,
                201,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = "{'message': 'License policy not found'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/license_policies/1001/copy/",
                post_data,
                404,
                expected_data,
                no_second_user=True,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_external",
                "post",
                "/api/license_policies/1001/copy/",
                post_data,
                403,
                expected_data,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/license_policies/1002/",
                None,
                204,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/license_policies/1000/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )

        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/license_policies/1001/",
                None,
                403,
                None,
                no_second_user=True,
            )
        )
