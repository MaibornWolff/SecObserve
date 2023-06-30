from unittest.mock import patch

from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from unittests.base_test_case import BaseTestCase


class TestViews(BaseTestCase):
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_version(self, mock_authentication):
        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.get("/api/status/version/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual({"version": "unittest_version"}, response.data)

    def test_health(self):
        api_client = APIClient()
        response = api_client.get("/api/status/health/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(None, response.data)

    def test_empty(self):
        api_client = APIClient()
        response = api_client.get("/")

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

    # --- NotificationViewSet ---

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_notification_bulk_delete_no_list(self, mock_authentication):
        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.post("/api/notifications/bulk_delete/")

        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"message": "Notifications: This field is required."}, response.data
        )

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.commons.api.views.bulk_delete")
    def test_notification_bulk_delete_successful(
        self, mock_bulk_delete, mock_authentication
    ):
        mock_authentication.return_value = self.user_internal, None

        data = {"notifications": [1, 2, 3]}
        api_client = APIClient()
        response = api_client.post(
            "/api/notifications/bulk_delete/", data=data, format="json"
        )

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)
        mock_bulk_delete.assert_called_once_with([1, 2, 3])
