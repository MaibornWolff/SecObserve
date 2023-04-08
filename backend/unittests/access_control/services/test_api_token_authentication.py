from itertools import chain
from unittest.mock import patch

from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_LOW_MEMORY
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from application.access_control.models import API_Token
from application.access_control.services.api_token_authentication import (
    APITokenAuthentication,
    create_api_token,
    revoke_api_token,
)
from unittests.base_test_case import BaseTestCase


class TestFunctions(BaseTestCase):
    @patch("application.access_control.models.API_Token.objects.get")
    def test_create_api_token_exists(self, mock):
        mock.return_value = API_Token()

        with self.assertRaises(ValidationError):
            create_api_token(self.user_internal)
            mock.assert_called_with(self.user_internal)

    @patch("application.access_control.models.API_Token.objects.get")
    @patch("application.access_control.models.API_Token.save")
    def test_create_api_token_new(self, save_mock, get_mock):
        get_mock.side_effect = API_Token.DoesNotExist()

        api_token = create_api_token(self.user_internal)

        self.assertEqual(32, len(api_token))
        get_mock.assert_called_with(user=self.user_internal)
        save_mock.assert_called()

    @patch("application.access_control.models.API_Token.objects.filter")
    @patch("application.access_control.models.API_Token.delete")
    def test_revoke_api_token(self, delete_mock, filter_mock):
        none_qs = API_Token.objects.none()
        api_token_1 = API_Token()
        api_token_2 = API_Token()
        qs = list(chain(none_qs, [api_token_1, api_token_2]))
        filter_mock.return_value = qs

        revoke_api_token(self.user_internal)

        filter_mock.assert_called_with(user=self.user_internal)
        self.assertEqual(2, delete_mock.call_count)


class TestAPITokenAuthentication(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.api_token = "api_token"
        ph = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)
        api_token_hash = ph.hash(self.api_token)

        api_token_object = API_Token(
            user=self.user_internal, api_token_hash=api_token_hash
        )
        self.api_tokens = [api_token_object]

    # --- authenticate_header ---

    def test_authenticate_header(self):
        api_token_authentication = APITokenAuthentication()
        self.assertEqual("APIToken", api_token_authentication.authenticate_header(None))

    # --- validate_api_token ---

    @patch("application.access_control.models.API_Token.objects.all")
    def test_validate_api_token_none(self, mock):
        mock.return_value = self.api_tokens

        api_token_authentication = APITokenAuthentication()
        user = api_token_authentication._validate_api_token("sss")
        self.assertIsNone(user)

    @patch("application.access_control.models.API_Token.objects.all")
    def test_validate_api_token_found(self, mock):
        mock.return_value = self.api_tokens

        api_token_authentication = APITokenAuthentication()
        user = api_token_authentication._validate_api_token(self.api_token)
        self.assertEqual(self.user_internal, user)

    # --- authenticate ---

    def test_authenticate_no_header(self):
        request = HttpRequest()
        api_token_authentication = APITokenAuthentication()
        user = api_token_authentication.authenticate(request)

        self.assertIsNone(user)

    def test_authenticate_invalid_header_1(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header"
        with self.assertRaises(AuthenticationFailed) as e:
            api_token_authentication = APITokenAuthentication()
            api_token_authentication.authenticate(request)

        self.assertEqual(
            "Invalid token header: No credentials provided.", str(e.exception)
        )

    def test_authenticate_invalid_header_spaces(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header token_1 token_2"
        with self.assertRaises(AuthenticationFailed) as e:
            api_token_authentication = APITokenAuthentication()
            api_token_authentication.authenticate(request)

        self.assertEqual(
            "Invalid token header: Token string should not contain spaces.",
            str(e.exception),
        )

    def test_authenticate_wrong_header(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header token"
        api_token_authentication = APITokenAuthentication()
        user = api_token_authentication.authenticate(request)

        self.assertIsNone(user)

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication._validate_api_token"
    )
    def test_authenticate_wrong_token(self, mock):
        mock.return_value = None

        with self.assertRaises(AuthenticationFailed) as e:
            request = HttpRequest()
            request.META["HTTP_AUTHORIZATION"] = b"APIToken token"
            api_token_authentication = APITokenAuthentication()
            api_token_authentication.authenticate(request)

        self.assertEqual("Invalid API token.", str(e.exception))

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication._validate_api_token"
    )
    def test_authenticate_user_deactivated(self, mock):
        mock.return_value = self.user_internal
        self.user_internal.is_active = False

        with self.assertRaises(AuthenticationFailed) as e:
            request = HttpRequest()
            request.META["HTTP_AUTHORIZATION"] = b"APIToken token"
            api_token_authentication = APITokenAuthentication()
            api_token_authentication.authenticate(request)

        self.assertEqual("User is deactivated.", str(e.exception))

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication._validate_api_token"
    )
    def test_authenticate_successful(self, mock):
        mock.return_value = self.user_internal

        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"APIToken token"
        api_token_authentication = APITokenAuthentication()
        user, _ = api_token_authentication.authenticate(request)

        self.assertEqual(self.user_internal, user)
