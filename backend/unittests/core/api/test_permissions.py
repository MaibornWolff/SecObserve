from unittest.mock import patch

from django.http.request import HttpRequest
from rest_framework.exceptions import ValidationError

from application.access_control.services.roles_permissions import Roles
from application.core.api.permissions import UserHasProductMemberPermission
from application.core.models import Product_Member
from unittests.base_test_case import BaseTestCase


class TestPermissions(BaseTestCase):
    @patch("application.core.api.permissions.get_highest_user_role")
    def test_has_object_permission_delete_owner_no_product_member(self, mock_get_highest_user_role):
        mock_get_highest_user_role.return_value = None

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(product=self.product_1, user=self.user_external, role=Roles.Owner)

        user_has_product_permission = UserHasProductMemberPermission()

        with self.assertRaises(ValidationError) as e:
            user_has_product_permission.has_object_permission(request=request, view=None, obj=product_member)

        self.assertEqual(
            "[ErrorDetail(string='You are not permitted to delete an Owner', code='invalid')]",
            str(e.exception),
        )
        mock_get_highest_user_role.assert_called_with(self.product_1, self.user_internal)

    @patch("application.core.api.permissions.get_highest_user_role")
    def test_has_object_permission_delete_owner_not_owner(self, mock_get_highest_user_role):
        mock_get_highest_user_role.return_value = 4

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(product=self.product_1, user=self.user_external, role=Roles.Owner)

        user_has_product_permission = UserHasProductMemberPermission()

        with self.assertRaises(ValidationError) as e:
            user_has_product_permission.has_object_permission(request=request, view=None, obj=product_member)

        self.assertEqual(
            "[ErrorDetail(string='You are not permitted to delete an Owner', code='invalid')]",
            str(e.exception),
        )
        mock_get_highest_user_role.assert_called_with(self.product_1, self.user_internal)

    @patch("application.core.api.permissions.get_highest_user_role")
    @patch("application.core.api.permissions.check_object_permission")
    def test_has_object_permission_delete_owner_success(self, mock_check, mock_get_highest_user_role):
        mock_check.return_value = True
        mock_get_highest_user_role.return_value = 5

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(product=self.product_1, user=self.user_external, role=Roles.Owner)

        user_has_product_permission = UserHasProductMemberPermission()

        self.assertTrue(
            user_has_product_permission.has_object_permission(request=request, view=None, obj=product_member)
        )
        mock_get_highest_user_role.assert_called_with(self.product_1, self.user_internal)
        mock_check.assert_called_once()
