from itertools import chain
from unittest.mock import patch

from rest_framework.exceptions import  ValidationError

from application.access_control.models import API_Token
from application.access_control.services.user_api_token import (
    create_user_api_token,
    revoke_user_api_token,
)
from unittests.base_test_case import BaseTestCase


class TestUserApiToken(BaseTestCase):
    @patch("application.access_control.models.API_Token.objects.get")
    def test_create_api_token_exists(self, mock):
        mock.return_value = API_Token()

        with self.assertRaises(ValidationError):
            create_user_api_token(self.user_internal)
            mock.assert_called_with(self.user_internal)

    @patch("application.access_control.models.API_Token.objects.get")
    @patch("application.access_control.models.API_Token.save")
    def test_create_api_token_new(self, save_mock, get_mock):
        get_mock.side_effect = API_Token.DoesNotExist()

        api_token = create_user_api_token(self.user_internal)

        self.assertEqual(42, len(api_token))
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

        revoke_user_api_token(self.user_internal)

        filter_mock.assert_called_with(user=self.user_internal)
        self.assertEqual(2, delete_mock.call_count)


