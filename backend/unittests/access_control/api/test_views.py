from unittest.mock import patch

from django.core.exceptions import ValidationError as DjangoValidationError
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.test import APIClient

from application.access_control.api.views import _get_authenticated_user
from unittests.base_test_case import BaseTestCase


class TestAPIToken(BaseTestCase):
    # --- create_user_api_token ---

    @patch("application.access_control.api.views._get_authenticated_user")
    def test_create_api_token_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(
            reverse("create_user_api_token"), request_data, "json"
        )

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views._get_authenticated_user")
    @patch("application.access_control.api.views.create_user_api_token")
    def test_create_api_token_view_validation_error(self, api_mock, user_mock):
        api_mock.side_effect = ValidationError(
            "Only one API token per user is allowed."
        )
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(
            reverse("create_user_api_token"), request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "Only one API token per user is allowed.", response.data["message"]
        )
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)

    @patch("application.access_control.api.views._get_authenticated_user")
    @patch("application.access_control.api.views.create_user_api_token")
    def test_create_api_token_view_successful(self, api_mock, user_mock):
        api_mock.return_value = "api_token"
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(
            reverse("create_user_api_token"), request_data, "json"
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual("api_token", response.data["token"])
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)

    # --- revoke_user_api_token ---

    @patch("application.access_control.api.views._get_authenticated_user")
    def test_revoke_api_token_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(
            reverse("revoke_user_api_token"), request_data, "json"
        )

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views._get_authenticated_user")
    @patch("application.access_control.api.views.revoke_user_api_token")
    def test_revoke_api_token_view_successful(self, api_mock, user_mock):
        user_mock.return_value = self.user_internal

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(
            reverse("revoke_user_api_token"), request_data, "json"
        )

        self.assertEqual(204, response.status_code)
        user_mock.assert_called_with(request_data)
        api_mock.assert_called_with(self.user_internal)


class TestAuthenticate(BaseTestCase):
    @patch("application.access_control.api.views._get_authenticated_user")
    def test_authenticate_view_not_authenticated(self, mock):
        mock.side_effect = PermissionDenied("Invalid credentials")

        api_client = APIClient()
        request_data = {"username": "user@example.com", "password": "not-so-secret"}
        response = api_client.post(reverse("authenticate"), request_data, "json")

        self.assertEqual(403, response.status_code)
        self.assertEqual("Invalid credentials", response.data["message"])
        mock.assert_called_with(request_data)

    @patch("application.access_control.api.views._get_authenticated_user")
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
            _get_authenticated_user(data)

    def test_get_authenticated_user_no_password(self):
        data = {"username": "user@example.com"}
        with self.assertRaises(ValidationError):
            _get_authenticated_user(data)

    @patch("application.access_control.api.views.django_authenticate")
    def test_get_authenticated_user_not_authenticated(self, mock):
        mock.return_value = None

        data = {"username": "user@example.com", "password": "not_so_secret"}
        with self.assertRaises(PermissionDenied) as e:
            _get_authenticated_user(data)

        self.assertEqual("Invalid credentials", str(e.exception))
        mock.assert_called_with(username="user@example.com", password="not_so_secret")

    @patch("application.access_control.api.views.django_authenticate")
    def test_get_authenticated_user_successful(self, mock):
        mock.return_value = self.user_internal

        data = {"username": "user@example.com", "password": "not_so_secret"}
        self.assertEqual(self.user_internal, _get_authenticated_user(data))
        mock.assert_called_with(username="user@example.com", password="not_so_secret")


class TestChangePassword(BaseTestCase):
    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    def test_change_password_unusable_password(
        self, save_mock, set_password_mock, get_object_mock, authentication_mock
    ):
        self.user_internal.set_unusable_password()
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new",
            "new_password_2": "new",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("User's password cannot be changed", response.data["message"])
        save_mock.assert_not_called()
        set_password_mock.assert_not_called()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    def test_change_password_oidc_user(
        self, save_mock, set_password_mock, get_object_mock, authentication_mock
    ):
        self.user_internal.is_oidc_user = True
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new",
            "new_password_2": "new",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("User's password cannot be changed", response.data["message"])
        save_mock.assert_not_called()
        set_password_mock.assert_not_called()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    def test_change_password_do_not_match(
        self, save_mock, set_password_mock, get_object_mock, authentication_mock
    ):
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new_1",
            "new_password_2": "new_2",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("The new passwords do not match", response.data["message"])
        save_mock.assert_not_called()
        set_password_mock.assert_not_called()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    @patch("application.access_control.api.views.django_authenticate")
    def test_change_password_current_password_incorrect(
        self,
        django_authenticate_mock,
        save_mock,
        set_password_mock,
        get_object_mock,
        authentication_mock,
    ):
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None
        django_authenticate_mock.return_value = None

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new",
            "new_password_2": "new",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("Current password is incorrect", response.data["message"])
        django_authenticate_mock.assert_called_with(
            username="user_admin@example.com", password="current"
        )
        save_mock.assert_not_called()
        set_password_mock.assert_not_called()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    @patch("application.access_control.api.views.django_authenticate")
    @patch("application.access_control.api.views.validate_password")
    def test_change_password_not_valid(
        self,
        validate_password_mock,
        django_authenticate_mock,
        save_mock,
        set_password_mock,
        get_object_mock,
        authentication_mock,
    ):
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None
        django_authenticate_mock.return_value = self.user_admin
        validate_password_mock.side_effect = DjangoValidationError(
            ["too_short", "too_common"]
        )

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new",
            "new_password_2": "new",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("too_short / too_common", response.data["message"])
        django_authenticate_mock.assert_called_with(
            username="user_admin@example.com", password="current"
        )
        save_mock.assert_not_called()
        set_password_mock.assert_not_called()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    @patch("application.access_control.api.views.UserViewSet.get_object")
    @patch("application.access_control.models.User.set_password")
    @patch("application.access_control.models.User.save")
    @patch("application.access_control.api.views.django_authenticate")
    @patch("application.access_control.api.views.validate_password")
    def test_change_password_successful(
        self,
        validate_password_mock,
        django_authenticate_mock,
        save_mock,
        set_password_mock,
        get_object_mock,
        authentication_mock,
    ):
        get_object_mock.return_value = self.user_internal
        authentication_mock.return_value = self.user_admin, None
        django_authenticate_mock.return_value = self.user_admin
        validate_password_mock.return_value = None

        api_client = APIClient()
        request_data = {
            "current_password": "current",
            "new_password_1": "new",
            "new_password_2": "new",
        }
        response = api_client.patch(
            "/api/users/123/change_password/", request_data, "json"
        )

        self.assertEqual(204, response.status_code)
        self.assertEqual(None, response.data)
        django_authenticate_mock.assert_called_with(
            username="user_admin@example.com", password="current"
        )
        save_mock.assert_called()
        set_password_mock.assert_called_with("new")
