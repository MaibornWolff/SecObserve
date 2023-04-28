from itertools import chain
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token, User
from application.access_control.services.product_api_token import (
    create_product_api_token,
    get_product_api_tokens,
    revoke_product_api_token,
)
from application.access_control.services.roles_permissions import Roles
from application.core.models import Product_Member
from unittests.base_test_case import BaseTestCase


class TestProductApiToken(BaseTestCase):
    @patch("application.access_control.services.product_api_token.get_user_by_username")
    def test_create_product_api_token_exists(self, mock):
        mock.return_value = User()

        with self.assertRaises(ValidationError):
            create_product_api_token(self.product_1, Roles.Upload)
            mock.assert_called_with("-product-None-api_token-")

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token.save")
    @patch("application.access_control.models.User.save")
    @patch("application.core.models.Product_Member.save")
    def test_create_product_api_token_new(
        self, product_member_save_mock, user_save_mock, api_token_save_mock, user_mock
    ):
        user_mock.return_value = None

        api_token = create_product_api_token(self.product_1, Roles.Upload)

        self.assertEqual(42, len(api_token))

        user_mock.assert_called_with("-product-None-api_token-")
        api_token_save_mock.assert_called()
        user_save_mock.assert_called()
        product_member_save_mock.assert_called()

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token.objects.filter")
    def test_revoke_product_api_token_not_exists(self, filter_mock, user_mock):
        user_mock.return_value = None
        revoke_product_api_token(self.user_internal)

        user_mock.assert_called_with("-product-None-api_token-")
        filter_mock.assert_not_called()

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token.objects.filter")
    @patch("application.access_control.models.API_Token.delete")
    @patch("application.access_control.models.User.delete")
    @patch("application.core.models.Product_Member.delete")
    @patch("application.access_control.services.product_api_token.get_product_member")
    def test_revoke_product_api_token(
        self,
        get_product_member_mock,
        product_member_delete_mock,
        user_delete_mock,
        api_token_delete_mock,
        filter_mock,
        user_mock,
    ):
        user = User()
        user_mock.return_value = user

        none_qs = API_Token.objects.none()
        api_token_1 = API_Token()
        api_token_2 = API_Token()
        qs = list(chain(none_qs, [api_token_1, api_token_2]))
        filter_mock.return_value = qs

        get_product_member_mock.return_value = Product_Member()

        revoke_product_api_token(self.product_1)

        user_mock.assert_called_with("-product-None-api_token-")
        filter_mock.assert_called_with(user=user)
        self.assertEqual(2, api_token_delete_mock.call_count)
        self.assertEqual(1, product_member_delete_mock.call_count)
        user_delete_mock.assert_called()

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    def test_get_product_api_tokens_no_user(self, user_mock):
        user_mock.return_value = None
        get_product_api_tokens(self.product_1)

        user_mock.assert_called_with("-product-None-api_token-")

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    @patch("application.access_control.services.product_api_token.get_product_member")
    def test_get_product_api_tokens_no_product_member(
        self, product_member_mock, user_mock
    ):
        user = User()
        user_mock.return_value = user

        product_member_mock.return_value = None

        get_product_api_tokens(self.product_1)

        user_mock.assert_called_with("-product-None-api_token-")
        product_member_mock.assert_called_with(self.product_1, user)

    @patch("application.access_control.services.product_api_token.get_user_by_username")
    @patch("application.access_control.services.product_api_token.get_product_member")
    def test_get_product_api_tokens_success(self, product_member_mock, user_mock):
        user = User()
        user_mock.return_value = user

        product_member_mock.return_value = Product_Member(role=Roles.Upload)

        product_api_tokens = get_product_api_tokens(self.product_1)

        self.assertEqual(1, len(product_api_tokens))
        self.assertEqual(self.product_1.pk, product_api_tokens[0].id)
        self.assertEqual(Roles.Upload, product_api_tokens[0].role)

        user_mock.assert_called_with("-product-None-api_token-")
        product_member_mock.assert_called_with(self.product_1, user)
