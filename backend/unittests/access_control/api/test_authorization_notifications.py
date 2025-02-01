from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.access_control.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationNotifications(TestAuthorizationBase):
    def test_authorization_notifications_product_member(self):
        self._test_authorization_notifications()

    def test_authorization_notifications_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_notifications()

    def _test_authorization_notifications(self):
        expected_data = "{'count': 6, 'next': None, 'previous': None, 'results': [{'id': 1, 'message': 'message_exception_internal', 'product_name': 'db_product_internal', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_internal_write', 'name': 'exception_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Exception', 'function': '', 'arguments': '', 'user': 2, 'product': 1, 'observation': 1}, {'id': 2, 'message': 'message_exception_external', 'product_name': 'db_product_external', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_external', 'name': 'exception_external', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Exception', 'function': '', 'arguments': '', 'user': 4, 'product': 2, 'observation': 2}, {'id': 3, 'message': '', 'product_name': 'db_product_internal', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_internal_write', 'name': 'security_gate_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Security gate', 'function': '', 'arguments': '', 'user': 2, 'product': 1, 'observation': 1}, {'id': 4, 'message': '', 'product_name': 'db_product_external', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_external', 'name': 'security_gate_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Security gate', 'function': '', 'arguments': '', 'user': 4, 'product': 2, 'observation': 2}, {'id': 5, 'message': 'message_task_internal', 'product_name': 'db_product_internal', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_internal_write', 'name': 'task_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Task', 'function': 'function_task_internal', 'arguments': 'arguments_task_internal', 'user': 2, 'product': 1, 'observation': 1}, {'id': 6, 'message': 'message_task_external', 'product_name': 'db_product_external', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_external', 'name': 'task_external', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Task', 'function': 'function_task_external', 'arguments': 'arguments_task_external', 'user': 4, 'product': 2, 'observation': 2}]}"
        self._test_api(
            APITest("db_admin", "get", "/api/notifications/", None, 200, expected_data)
        )

        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 3, 'message': '', 'product_name': 'db_product_internal', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_internal_write', 'name': 'security_gate_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Security gate', 'function': '', 'arguments': '', 'user': 2, 'product': 1, 'observation': 1}, {'id': 5, 'message': '...', 'product_name': 'db_product_internal', 'observation_title': 'db_observation_internal', 'user_full_name': 'db_internal_write', 'name': 'task_internal', 'created': '2022-12-15T17:10:35.518000+01:00', 'type': 'Task', 'function': 'function_task_internal', 'arguments': 'arguments_task_internal', 'user': 2, 'product': 1, 'observation': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/notifications/",
                None,
                200,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/notifications/1/", None, 404, None
            )
        )

        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/notifications/3/", None, 200, None
            )
        )

        post_data = {"notifications": [1, 3, 5]}
        expected_data = "{'message': 'Some notifications do not exist'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/notifications/bulk_mark_as_read/",
                post_data,
                400,
                expected_data,
            )
        )
