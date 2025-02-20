from unittest.mock import patch

from django.core.management import call_command
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from application.access_control.queries.user import get_user_by_username
from application.commons.models import Notification_Viewed
from unittests.base_test_case import BaseTestCase


class TestViews(BaseTestCase):
    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
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

    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    def test_notification_bulk_mark_as_viewed_no_list(self, mock_authentication):
        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.post("/api/notifications/bulk_mark_as_viewed/")

        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({"message": "Notifications: This field is required."}, response.data)

    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    def test_notification_bulk_mark_as_viewed_successful(self, mock_authentication):
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")
        # mock_authentication.return_value = self.user_internal, None
        user = get_user_by_username("db_internal_write")
        mock_authentication.return_value = user, None

        data = {"notifications": [3, 5]}
        api_client = APIClient()
        response = api_client.post("/api/notifications/bulk_mark_as_viewed/", data=data, format="json")

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

        notification_viewed = Notification_Viewed.objects.get(notification_id=3, user=user)
        self.assertIsNotNone(notification_viewed)

        notification_viewed = Notification_Viewed.objects.get(notification_id=5, user=user)
        self.assertIsNotNone(notification_viewed)

    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    def test_notification_mark_as_viewed_not_found(self, mock_authentication):
        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.post("/api/notifications/99999/mark_as_viewed/")

        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    @patch("application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate")
    def test_notification_mark_as_viewed_successful(self, mock_authentication):
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")

        mock_authentication.return_value = self.user_internal, None

        api_client = APIClient()
        response = api_client.post("/api/notifications/1/mark_as_viewed/")

        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

        notification_viewed = Notification_Viewed.objects.get(notification_id=1, user=self.user_internal)
        self.assertIsNotNone(notification_viewed)
