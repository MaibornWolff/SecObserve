from datetime import timedelta
from unittest.mock import patch

import jwt
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from application.access_control.models import User
from application.access_control.services.oauth2_authentication import (
    OAuth2Authentication,
)
from unittests.base_test_case import BaseTestCase


class TestOAuth2Authentication(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    # --- authenticate ---

    def test_authenticate_no_header(self):
        request = HttpRequest()
        oauth2_authentication = OAuth2Authentication()
        user = oauth2_authentication.authenticate(request)

        self.assertIsNone(user)

    def test_authenticate_invalid_header_1(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header"
        with self.assertRaises(AuthenticationFailed) as e:
            oauth2_authentication = OAuth2Authentication()
            oauth2_authentication.authenticate(request)

        self.assertEqual(
            "Invalid token header: No credentials provided.", str(e.exception)
        )

    def test_authenticate_invalid_header_spaces(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header token_1 token_2"
        with self.assertRaises(AuthenticationFailed) as e:
            oauth2_authentication = OAuth2Authentication()
            oauth2_authentication.authenticate(request)

        self.assertEqual(
            "Invalid token header: Token string should not contain spaces.",
            str(e.exception),
        )

    def test_authenticate_wrong_header(self):
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"header token"
        oauth2_authentication = OAuth2Authentication()
        user = oauth2_authentication.authenticate(request)

        self.assertIsNone(user)

    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._validate_jwt"
    )
    def test_authenticate_wrong_token(self, mock):
        mock.return_value = None

        with self.assertRaises(AuthenticationFailed) as e:
            request = HttpRequest()
            request.META["HTTP_AUTHORIZATION"] = b"Bearer token"
            oauth2_authentication = OAuth2Authentication()
            oauth2_authentication.authenticate(request)

        self.assertEqual("Invalid token.", str(e.exception))

    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._validate_jwt"
    )
    def test_authenticate_user_deactivated(self, mock):
        mock.return_value = self.user_internal
        self.user_internal.is_active = False

        with self.assertRaises(AuthenticationFailed) as e:
            request = HttpRequest()
            request.META["HTTP_AUTHORIZATION"] = b"Bearer token"
            oauth2_authentication = OAuth2Authentication()
            oauth2_authentication.authenticate(request)

        self.assertEqual("User is deactivated.", str(e.exception))

        self.user_internal.is_active = True

    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._validate_jwt"
    )
    def test_authenticate_successful(self, mock):
        mock.return_value = self.user_internal

        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = b"Bearer token"
        oauth2_authentication = OAuth2Authentication()
        user, _ = oauth2_authentication.authenticate(request)

        self.assertEqual(self.user_internal, user)

    # --- authenticate_header ---

    def test_authenticate_header(self):
        oauth2_authentication = OAuth2Authentication()
        self.assertEqual("Bearer", oauth2_authentication.authenticate_header(None))

    # --- _validate_jwt ---

    @patch("jwt.decode")
    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._get_jwks_uri"
    )
    @patch("jwt.PyJWKClient.__init__")
    @patch("jwt.PyJWKClient.get_signing_key_from_jwt")
    def test_validate_jwt_message(
        self, get_signing_key_mock, pyjwkclient_mock, jwks_uri_mock, jwt_mock
    ):
        jwks_uri_mock.return_value = "test_jwks_uri"
        pyjwkclient_mock.return_value = None
        mock_py_jwk = MockPyJWK("test_key")
        get_signing_key_mock.return_value = mock_py_jwk
        jwt_mock.side_effect = jwt.ExpiredSignatureError("Signature expired")

        with self.assertRaises(AuthenticationFailed) as e:
            oauth2_authentication = OAuth2Authentication()
            oauth2_authentication._validate_jwt("token")

        self.assertEqual("Signature expired", str(e.exception))
        jwks_uri_mock.assert_called_once()
        pyjwkclient_mock.assert_called_once_with("test_jwks_uri")
        get_signing_key_mock.assert_called_once_with("token")
        jwt_mock.assert_called_with(
            jwt="token",
            key="test_key",
            options={"verify_aud": False},
            algorithms=["RS256", "RS384", "RS512", "ES256 ", "ES384", "ES512", "EdDSA"],
        )

    @patch("jwt.decode")
    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._get_jwks_uri"
    )
    @patch("jwt.PyJWKClient.__init__")
    @patch("jwt.PyJWKClient.get_signing_key_from_jwt")
    @patch(
        "application.access_control.services.oauth2_authentication.get_user_by_username"
    )
    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._create_user"
    )
    def test_validate_jwt_user_not_found(
        self,
        create_user_mock,
        get_user_mock,
        get_signing_key_mock,
        pyjwkclient_mock,
        jwks_uri_mock,
        jwt_mock,
    ):
        jwks_uri_mock.return_value = "test_jwks_uri"
        pyjwkclient_mock.return_value = None
        mock_py_jwk = MockPyJWK("test_key")
        get_signing_key_mock.return_value = mock_py_jwk
        jwt_mock.return_value = {"preferred_username": "test_username"}
        get_user_mock.return_value = None
        expected_user = User(username="test_username")
        create_user_mock.return_value = expected_user

        oauth2_authentication = OAuth2Authentication()
        user = oauth2_authentication._validate_jwt("token")

        self.assertEqual(user, expected_user)
        get_user_mock.assert_called_with("test_username")
        jwks_uri_mock.assert_called_once()
        pyjwkclient_mock.assert_called_once_with("test_jwks_uri")
        get_signing_key_mock.assert_called_once_with("token")
        jwt_mock.assert_called_with(
            jwt="token",
            key="test_key",
            options={"verify_aud": False},
            algorithms=["RS256", "RS384", "RS512", "ES256 ", "ES384", "ES512", "EdDSA"],
        )
        create_user_mock.assert_called_once_with(
            "test_username", {"preferred_username": "test_username"}
        )

    @patch("jwt.decode")
    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._get_jwks_uri"
    )
    @patch("jwt.PyJWKClient.__init__")
    @patch("jwt.PyJWKClient.get_signing_key_from_jwt")
    @patch(
        "application.access_control.services.oauth2_authentication.get_user_by_username"
    )
    @patch(
        "application.access_control.services.oauth2_authentication.OAuth2Authentication._check_user_change"
    )
    def test_validate_jwt_user_found(
        self,
        check_user_change_mock,
        get_user_mock,
        get_signing_key_mock,
        pyjwkclient_mock,
        jwks_uri_mock,
        jwt_mock,
    ):
        jwks_uri_mock.return_value = "test_jwks_uri"
        pyjwkclient_mock.return_value = None
        mock_py_jwk = MockPyJWK("test_key")
        get_signing_key_mock.return_value = mock_py_jwk
        jwt_mock.return_value = {"preferred_username": self.user_internal.username}
        get_user_mock.return_value = self.user_internal
        check_user_change_mock.return_value = self.user_internal

        oauth2_authentication = OAuth2Authentication()
        user = oauth2_authentication._validate_jwt("token")

        self.assertEqual(self.user_internal, user)
        get_user_mock.assert_called_with(self.user_internal.username)
        jwks_uri_mock.assert_called_once()
        pyjwkclient_mock.assert_called_once_with("test_jwks_uri")
        get_signing_key_mock.assert_called_once_with("token")
        jwt_mock.assert_called_with(
            jwt="token",
            key="test_key",
            options={"verify_aud": False},
            algorithms=["RS256", "RS384", "RS512", "ES256 ", "ES384", "ES512", "EdDSA"],
        )
        check_user_change_mock.assert_called_once_with(
            self.user_internal, {"preferred_username": self.user_internal.username}
        )

    @patch("requests.request")
    def test_get_jwks_uri(self, requests_mock):
        requests_mock.return_value = MockResponse()
        oauth2_authentication = OAuth2Authentication()
        jwks_uri = oauth2_authentication._get_jwks_uri()

        self.assertEqual("https://authority/.well-known/jwks.json", jwks_uri)
        requests_mock.assert_called_once_with(
            method="GET",
            url="https://authority/.well-known/openid-configuration",
            timeout=60,
        )

    @patch("application.access_control.services.oauth2_authentication.User.save")
    def test_create_user(self, user_save_mock):
        oauth2_authentication = OAuth2Authentication()
        user = oauth2_authentication._create_user(
            "test_username",
            {
                "preferred_username": "test_username",
                "given_name": "test_first_name",
                "family_name": "test_last_name",
                "email": "test_email",
            },
        )

        self.assertEqual("test_username", user.username)
        self.assertEqual("test_first_name", user.first_name)
        self.assertEqual("test_last_name", user.last_name)
        self.assertEqual("test_email", user.email)
        user_save_mock.assert_called_once()

    @patch("application.access_control.services.oauth2_authentication.User.save")
    def test_check_user_change_no_change(self, user_save_mock):
        old_user = User(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email",
        )
        oauth2_authentication = OAuth2Authentication()
        new_user = oauth2_authentication._check_user_change(
            old_user,
            {
                "preferred_username": "test_username",
                "given_name": "test_first_name",
                "family_name": "test_last_name",
                "email": "test_email",
            },
        )

        self.assertEqual("test_username", new_user.username)
        self.assertEqual("test_first_name", new_user.first_name)
        self.assertEqual("test_last_name", new_user.last_name)
        self.assertEqual("test_email", new_user.email)
        user_save_mock.assert_not_called()

    @patch("application.access_control.services.oauth2_authentication.User.save")
    def test_check_user_change_with_changes(self, user_save_mock):
        old_user = User(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email",
        )
        oauth2_authentication = OAuth2Authentication()
        new_user = oauth2_authentication._check_user_change(
            old_user,
            {
                "preferred_username": "test_username",
                "given_name": "test_first_name_new",
                "family_name": "test_last_name_new",
                "email": "test_email_new",
            },
        )

        self.assertEqual("test_username", new_user.username)
        self.assertEqual("test_first_name_new", new_user.first_name)
        self.assertEqual("test_last_name_new", new_user.last_name)
        self.assertEqual("test_email_new", new_user.email)
        user_save_mock.assert_called_once()


class MockPyJWK:
    def __init__(self, key):
        self.key = key


class MockResponse:
    def __init__(self):
        self.raise_for_status_called = False

    def raise_for_status(self):
        self.raise_for_status_called = True

    def json(self):
        if not self.raise_for_status_called:
            raise Exception("raise_for_status not called")
        return {"jwks_uri": "https://authority/.well-known/jwks.json"}
