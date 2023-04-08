from unittest.mock import patch
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.test import APIClient
from django.urls import reverse

from unittests.base_test_case import BaseTestCase
from application.access_control.api.views import get_authenticated_user


class TestAPIToken(BaseTestCase):
    # --- create_api_token ---

    @patch("application.access_control.api.views.get_authenticated_user")
    def test_create_api_token_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("create_api_token"), request_data, "json")

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views.get_authenticated_user")
    @patch("application.access_control.api.views.create_api_token")
    def test_create_api_token_view_validation_error(self, api_mock, user_mock):
        api_mock.side_effect = ValidationError(
            "Only one API token per user is allowed."
        )
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("create_api_token"), request_data, "json")

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "Only one API token per user is allowed.", response.data["message"]
        )
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)

    @patch("application.access_control.api.views.get_authenticated_user")
    @patch("application.access_control.api.views.create_api_token")
    def test_create_api_token_view_successful(self, api_mock, user_mock):
        api_mock.return_value = "api_token"
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("create_api_token"), request_data, "json")
        self.assertEqual(200, response.status_code)
        self.assertEqual("api_token", response.data["token"])
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)

    # --- revoke_api_token ---

    @patch("application.access_control.api.views.get_authenticated_user")
    def test_revoke_api_token_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("revoke_api_token"), request_data, "json")

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views.get_authenticated_user")
    @patch("application.access_control.api.views.revoke_api_token")
    def test_revoke_api_token_view_successful(self, api_mock, user_mock):
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("revoke_api_token"), request_data, "json")

        self.assertEqual(204, response.status_code)
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)


class TestAuthenticate(BaseTestCase):
    @patch("application.access_control.api.views.get_authenticated_user")
    def test_authenticate_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("authenticate"), request_data, "json")

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views.get_authenticated_user")
    @patch("application.access_control.api.views.create_jwt")
    def test_authenticate_view_successful(self, jwt_mock, user_mock):
        jwt_mock.return_value = "token"
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("authenticate"), request_data, "json")

        self.assertEqual(200, response.status_code)
        self.assertEqual("token", response.data["jwt"])
        self.assertEqual(self.user_internal.username, response.data["user"]["username"])
        user_mock.assert_called_with(request_data)
        jwt_mock.assert_called_with(self.user_internal)


class TestGetAuthenticatedUser(BaseTestCase):
    def test_get_authenticated_user_no_user(self):
        data = {"password": "not_so_secret"}
        with self.assertRaises(ValidationError):
            get_authenticated_user(data)

    def test_get_authenticated_user_no_password(self):
        data = {"username": "user@example.com"}
        with self.assertRaises(ValidationError):
            get_authenticated_user(data)

    @patch("application.access_control.api.views.django_authenticate")
    def test_get_authenticated_user_not_authenticated(self, mock):
        mock.return_value = None

        data = {"username": "user@example.com", "password": "not_so_secret"}
        with self.assertRaises(PermissionDenied) as e:
            get_authenticated_user(data)

        self.assertEqual("Invalid credentials", str(e.exception))
        mock.assert_called_with(username="user@example.com", password="not_so_secret")

    @patch("application.access_control.api.views.django_authenticate")
    def test_get_authenticated_user_successful(self, mock):
        mock.return_value = self.user_internal

        data = {"username": "user@example.com", "password": "not_so_secret"}
        self.assertEqual(self.user_internal, get_authenticated_user(data))
        mock.assert_called_with(username="user@example.com", password="not_so_secret")
