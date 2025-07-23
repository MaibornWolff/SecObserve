from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationPeriodicTasks(TestAuthorizationBase):

    def test_authorization_periodic_tasks(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'task': 'Calculate product metrics', 'start_time': '2022-12-15T17:10:35.513000+01:00', 'duration': 1234, 'status': 'Success', 'message': 'Task completed successfully'}, {'id': 2, 'task': 'Calculate product metrics', 'start_time': '2022-12-16T17:10:35.513000+01:00', 'duration': 5678, 'status': 'Failure', 'message': 'Exception has occurred'}]}"
        self._test_api(APITest("db_admin", "get", "/api/periodic_tasks/", None, 200, expected_data))

        expected_data = "{'id': 1, 'task': 'Calculate product metrics', 'start_time': '2022-12-15T17:10:35.513000+01:00', 'duration': 1234, 'status': 'Success', 'message': 'Task completed successfully'}"
        self._test_api(APITest("db_admin", "get", "/api/periodic_tasks/1/", None, 200, expected_data))

        self._test_api(APITest("db_internal_write", "get", "/api/periodic_tasks/", None, 403, None))

        self._test_api(APITest("db_internal_write", "get", "/api/periodic_tasks/1/", None, 403, None))
