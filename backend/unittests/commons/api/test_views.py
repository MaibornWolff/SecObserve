from unittest.mock import patch

from django.core.management import call_command
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from application.access_control.models import User
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


class TestNotificationViewset(BaseTestCase):
    def setUp(self) -> None:
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")
        return super().setUp()

    # --- GET list ---

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_get_notifications_admin(self, mock_authentication):
        mock_authentication.return_value = User.objects.get(pk=1), None

        api_client = APIClient()
        response = api_client.get("/api/notifications/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(5, response.data["count"])
        self.assertEqual(
            "db_notification_admin_full", response.data["results"][0]["name"]
        )
        self.assertEqual(
            "2022-12-15T17:10:35.518000+01:00", response.data["results"][0]["created"]
        )
        self.assertEqual(
            "message_db_notification_full", response.data["results"][0]["message"]
        )
        self.assertEqual(
            "function_db_notification_full", response.data["results"][0]["function"]
        )
        self.assertEqual(
            "arguments_db_notification_full", response.data["results"][0]["arguments"]
        )
        self.assertEqual(1, response.data["results"][0]["product"])
        self.assertEqual(1, response.data["results"][0]["observation"])
        self.assertEqual(1, response.data["results"][0]["user"])

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_get_notifications_user_internal(self, mock_authentication):
        mock_authentication.return_value = User.objects.get(pk=2), None

        api_client = APIClient()
        response = api_client.get("/api/notifications/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(2, response.data["count"])
        self.assertEqual(
            "db_notification_internal_full", response.data["results"][0]["name"]
        )
        self.assertEqual(
            "db_notification_internal_empty", response.data["results"][1]["name"]
        )

    # --- GET single ---

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_get_notification_user_internal_not_found_admin(self, mock_authentication):
        mock_authentication.return_value = User.objects.get(pk=2), None

        api_client = APIClient()
        response = api_client.get("/api/notifications/1/")

        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_get_notification_user_internal_not_found_wrong_product(
        self, mock_authentication
    ):
        mock_authentication.return_value = User.objects.get(pk=2), None

        api_client = APIClient()
        response = api_client.get("/api/notifications/4/")

        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_get_notification_user_internal_found(self, mock_authentication):
        mock_authentication.return_value = User.objects.get(pk=2), None

        api_client = APIClient()
        response = api_client.get("/api/notifications/2/")

        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual("db_notification_internal_full", response.data["name"])

    # --- bulk_delete ---

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.commons.api.views.bulk_delete")
    def test_bulk_delete(self, mock_bulk_delete, mock_authentication):
        mock_authentication.return_value = User.objects.get(pk=2), None

        data = {"notifications": [1, 2]}

        api_client = APIClient()
        response = api_client.delete(
            "/api/notifications/bulk_delete/", data=data, format="json"
        )

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)
        mock_bulk_delete.assert_called_once_with([1, 2])
