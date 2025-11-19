from datetime import date
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token_Multiple
from application.access_control.services.user_api_token import (
    create_user_api_token,
    revoke_user_api_token,
)
from unittests.base_test_case import BaseTestCase


class TestUserApiToken(BaseTestCase):
    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    def test_create_api_token_exists(self, mock):
        mock.return_value = API_Token_Multiple()

        with self.assertRaises(ValidationError):
            create_user_api_token(self.user_internal, "api_token_name", date.today())
            mock.assert_called_with(self.user_internal, name="api_token_name")

    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    @patch("application.access_control.models.API_Token_Multiple.save")
    def test_create_api_token_new(self, save_mock, get_mock):
        get_mock.side_effect = API_Token_Multiple.DoesNotExist()

        api_token = create_user_api_token(self.user_internal, "api_token_name", date.today())

        self.assertEqual(42, len(api_token))
        get_mock.assert_called_with(user=self.user_internal, name="api_token_name")
        save_mock.assert_called()

    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    @patch("application.access_control.models.API_Token_Multiple.delete")
    def test_revoke_api_token(self, delete_mock, get_mock):
        get_mock.return_value = API_Token_Multiple()

        revoke_user_api_token(self.user_internal, "api_token_name")

        get_mock.assert_called_with(user=self.user_internal, name="api_token_name")
        self.assertEqual(1, delete_mock.call_count)
