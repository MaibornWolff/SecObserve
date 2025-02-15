from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationVEXCounters(TestAuthorizationBase):
    def test_authorization_vex_counters(self):
        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'document_id_prefix': 'prefix', 'year': 2024, 'counter': 2}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/vex_counters/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'document_id_prefix': 'prefix', 'year': 2024, 'counter': 2}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/vex_counters/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No VEX_Counter matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/vex_counters/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"document_id_prefix": "string", "year": 2024}
        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/vex/vex_counters/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 2, 'document_id_prefix': 'string', 'year': 2024, 'counter': 0}"
        self._test_api(
            APITest(
                "db_admin",
                "post",
                "/api/vex/vex_counters/",
                post_data,
                201,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/vex/vex_counters/1/",
                {"counter": "5"},
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'document_id_prefix': 'prefix', 'year': 2024, 'counter': 7}"
        self._test_api(
            APITest(
                "db_admin",
                "patch",
                "/api/vex/vex_counters/1/",
                {"counter": "7"},
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/vex/vex_counters/1/",
                None,
                403,
                expected_data,
            )
        )

        expected_data = "None"
        self._test_api(
            APITest(
                "db_admin",
                "delete",
                "/api/vex/vex_counters/1/",
                None,
                204,
                expected_data,
            )
        )
