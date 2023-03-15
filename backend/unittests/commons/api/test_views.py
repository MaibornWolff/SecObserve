from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from unittests.base_test_case import BaseTestCase


class TestViews(BaseTestCase):
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_commit(self, mock_authentication):
        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.get("/api/status/commit_id/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual({"commit_id": "unittest_commit_id"}, response.data)

    def test_health(self):
        api_client = APIClient()
        response = api_client.get("/api/status/health/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(None, response.data)

    def test_empty(self):
        api_client = APIClient()
        response = api_client.get("/")

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)
