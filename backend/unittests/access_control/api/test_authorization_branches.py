from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationBranches(TestAuthorizationBase):
    def test_authorization_branches(self):
        expected_data = "OrderedDict({'count': 3, 'next': None, 'previous': None, 'results': [OrderedDict({'id': 1, 'name_with_product': 'db_branch_internal_dev (db_product_internal)', 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_dev', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}), OrderedDict({'id': 2, 'name_with_product': 'db_branch_internal_main (db_product_internal)', 'is_default_branch': False, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_main', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}), OrderedDict({'id': 3, 'name_with_product': 'db_branch_external (db_product_external)', 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_external', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 2})]})"
        self._test_api(
            APITest("db_admin", "get", "/api/branches/", None, 200, expected_data)
        )

        expected_data = "OrderedDict({'count': 2, 'next': None, 'previous': None, 'results': [OrderedDict({'id': 1, 'name_with_product': 'db_branch_internal_dev (db_product_internal)', 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_dev', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}), OrderedDict({'id': 2, 'name_with_product': 'db_branch_internal_main (db_product_internal)', 'is_default_branch': False, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_main', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1})]})"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'name_with_product': 'db_branch_internal_dev (db_product_internal)', 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_dev', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No Branch matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/3/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"name": "string", "product": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/branches/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 4, 'name_with_product': 'string (db_product_internal)', 'is_default_branch': False, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'string', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/branches/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"name": "changed"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/branches/1/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'name_with_product': 'changed (db_product_internal)', 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'changed', 'last_import': None, 'housekeeping_protect': False, 'purl': '', 'cpe23': '', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/branches/1/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/branches/1/",
                None,
                403,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You cannot delete the default branch of a product.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/branches/1/",
                None,
                400,
                expected_data,
            )
        )
