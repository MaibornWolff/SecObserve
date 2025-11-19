from datetime import date
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token_Multiple, User
from application.authorization.services.roles_permissions import Roles
from application.core.models import Product_Member
from application.core.services.product_api_token import (
    create_product_api_token,
    get_product_api_tokens,
    revoke_product_api_token,
)
from unittests.base_test_case import BaseTestCase


class TestProductApiToken(BaseTestCase):
    @patch("application.core.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    def test_create_product_api_token_exists(self, api_token_get_mock, user_mock):
        user = User()
        user_mock.return_value = user
        api_token_get_mock.return_value = None

        with self.assertRaises(ValidationError) as e:
            create_product_api_token(self.product_1, Roles.Upload, "api_token_name", date.today())
            user_mock.assert_called_with("-product-None-api_token_name-api_token-")
            api_token_get_mock.assert_called_with(user=user)
            self.assertEqual("API token with this name already exists.", str(e))

    @patch("application.core.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    @patch("application.access_control.models.API_Token_Multiple.save")
    @patch("application.access_control.models.User.save")
    @patch("application.core.models.Product_Member.save")
    @patch("application.access_control.models.User.set_unusable_password")
    def test_create_product_api_token_with_user(
        self,
        set_unusable_password_mock,
        product_member_save_mock,
        user_save_mock,
        api_token_save_mock,
        api_token_get_mock,
        user_mock,
    ):
        user = User()
        user_mock.return_value = user
        api_token_get_mock.side_effect = API_Token_Multiple.DoesNotExist()

        api_token = create_product_api_token(self.product_1, Roles.Upload, "api_token_name", date.today())

        self.assertEqual(42, len(api_token))

        user_mock.assert_called_with("-product-None-api_token_name-api_token-")
        api_token_get_mock.assert_called_with(user=user)
        api_token_save_mock.assert_called()
        user_save_mock.assert_called()
        product_member_save_mock.assert_called()
        set_unusable_password_mock.assert_called()

    @patch("application.core.services.product_api_token.get_user_by_username")
    @patch("application.access_control.models.API_Token_Multiple.save")
    @patch("application.access_control.models.User.save")
    @patch("application.core.models.Product_Member.save")
    @patch("application.access_control.models.User.set_unusable_password")
    def test_create_product_api_token_without_user(
        self,
        set_unusable_password_mock,
        product_member_save_mock,
        user_save_mock,
        api_token_save_mock,
        user_mock,
    ):
        user_mock.return_value = None

        api_token = create_product_api_token(self.product_1, Roles.Upload, "api_token_name", None)

        self.assertEqual(42, len(api_token))

        user_mock.assert_called_with("-product-None-api_token_name-api_token-")
        api_token_save_mock.assert_called()
        user_save_mock.assert_called()
        product_member_save_mock.assert_called()
        set_unusable_password_mock.assert_called()

    @patch("application.access_control.models.API_Token_Multiple.delete")
    @patch("application.access_control.models.User.save")
    @patch("application.core.models.Product_Member.delete")
    @patch("application.core.services.product_api_token.get_product_member")
    def test_revoke_product_no_product_member(
        self,
        get_product_member_mock,
        product_member_delete_mock,
        user_save_mock,
        api_token_delete_mock,
    ):
        user = User(username="username", full_name="full_name")
        api_token = API_Token_Multiple(user=user, api_token_hash="hash")
        get_product_member_mock.return_value = None

        revoke_product_api_token(self.product_1, api_token)

        api_token_delete_mock.assert_called()
        get_product_member_mock.assert_called_with(self.product_1, user)
        product_member_delete_mock.assert_not_called()
        user_save_mock.assert_called()

    @patch("application.access_control.models.API_Token_Multiple.delete")
    @patch("application.access_control.models.User.save")
    @patch("application.core.models.Product_Member.delete")
    @patch("application.core.services.product_api_token.get_product_member")
    def test_revoke_product_api_token(
        self,
        get_product_member_mock,
        product_member_delete_mock,
        user_save_mock,
        api_token_delete_mock,
    ):
        user = User(username="username", full_name="full_name")
        api_token = API_Token_Multiple(user=user, api_token_hash="hash")
        get_product_member_mock.return_value = Product_Member()

        revoke_product_api_token(self.product_1, api_token)

        api_token_delete_mock.assert_called()
        get_product_member_mock.assert_called_with(self.product_1, user)
        product_member_delete_mock.assert_called()
        user_save_mock.assert_called()

    @patch("application.access_control.models.User.objects.filter")
    def test_get_product_api_tokens_no_user(self, user_mock):
        user_mock.return_value = []

        product_api_tokens = get_product_api_tokens(self.product_1)

        self.assertEqual(0, len(product_api_tokens))
        user_mock.assert_called_with(username__startswith="-product-None-")

    @patch("application.access_control.models.User.objects.filter")
    @patch("application.core.services.product_api_token.get_product_member")
    def test_get_product_api_tokens_no_product_member(self, product_member_mock, user_mock):
        user = User()
        user_mock.return_value = [user]

        product_member_mock.return_value = None

        product_api_tokens = get_product_api_tokens(self.product_1)

        self.assertEqual(0, len(product_api_tokens))
        user_mock.assert_called_with(username__startswith="-product-None-")
        product_member_mock.assert_called_with(self.product_1, user)

    @patch("application.access_control.models.User.objects.filter")
    @patch("application.core.services.product_api_token.get_product_member")
    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    def test_get_product_api_tokens_no_api_token(self, api_token_mock, product_member_mock, user_mock):
        user = User()
        user_mock.return_value = [user]
        product_member_mock.return_value = Product_Member(role=Roles.Upload)
        api_token_mock.side_effect = API_Token_Multiple.DoesNotExist()

        product_api_tokens = get_product_api_tokens(self.product_1)

        self.assertEqual(0, len(product_api_tokens))
        user_mock.assert_called_with(username__startswith="-product-None-")
        product_member_mock.assert_called_with(self.product_1, user)
        api_token_mock.assert_called_with(user=user)

    @patch("application.access_control.models.User.objects.filter")
    @patch("application.core.services.product_api_token.get_product_member")
    @patch("application.access_control.models.API_Token_Multiple.objects.get")
    def test_get_product_api_tokens_success(self, api_token_mock, product_member_mock, user_mock):
        user = User()
        user_mock.return_value = [user]
        product_member_mock.return_value = Product_Member(role=Roles.Upload)
        expiration_date = date(2025, 11, 14)
        api_token = API_Token_Multiple(user=user, name="api_token_name", api_token_hash="hash", expiration_date=expiration_date)
        api_token_mock.return_value = api_token

        product_api_tokens = get_product_api_tokens(self.product_1)

        self.assertEqual(1, len(product_api_tokens))
        self.assertEqual(self.product_1.pk, product_api_tokens[0].id)
        self.assertEqual(Roles.Upload, product_api_tokens[0].role)
        self.assertEqual("api_token_name", product_api_tokens[0].name)
        self.assertEqual(expiration_date, product_api_tokens[0].expiration_date)

        user_mock.assert_called_with(username__startswith="-product-None-")
        product_member_mock.assert_called_with(self.product_1, user)
        api_token_mock.assert_called_with(user=user)
