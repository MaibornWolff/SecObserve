from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationServices(TestAuthorizationBase):
    def test_authorization_services(self):
        expected_data = "{'count': 3, 'next': None, 'previous': None, 'results': [{'id': 1, 'name_with_product': 'db_service_internal_backend (db_product_internal)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_internal_backend', 'product': 1}, {'id': 2, 'name_with_product': 'db_service_internal_frontend (db_product_internal)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_internal_frontend', 'product': 1}, {'id': 3, 'name_with_product': 'db_service_external (db_product_external)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_external', 'product': 2}]}"
        self._test_api(
            APITest("db_admin", "get", "/api/services/", None, 200, expected_data)
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'name_with_product': 'db_service_internal_backend (db_product_internal)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_internal_backend', 'product': 1}, {'id': 2, 'name_with_product': 'db_service_internal_frontend (db_product_internal)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_internal_frontend', 'product': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/services/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'name_with_product': 'db_service_internal_backend (db_product_internal)', 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_service_internal_backend', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/services/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No Service matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/services/3/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/services/99999/",
                None,
                404,
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
                "/api/services/1/",
                None,
                403,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'Cannot delete Service because it still has Observations.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/services/1/",
                None,
                409,
                expected_data,
            )
        )
