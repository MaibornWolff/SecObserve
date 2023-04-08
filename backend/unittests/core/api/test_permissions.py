from unittest.mock import patch

from django.http.request import HttpRequest

from application.access_control.services.roles_permissions import Roles
from application.core.api.permissions import UserHasProductMemberPermission
from application.core.models import Product_Member
from unittests.base_test_case import BaseTestCase


class TestPermissions(BaseTestCase):
    @patch("application.core.api.permissions.get_product_member")
    def test_has_object_permission_delete_owner_no_product_member(
        self, mock_get_product_member
    ):
        mock_get_product_member.return_value = None

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(
            product=self.product_1, user=self.user_external, role=Roles.Owner
        )

        user_has_product_permission = UserHasProductMemberPermission()

        self.assertFalse(
            user_has_product_permission.has_object_permission(
                request=request, view=None, obj=product_member
            )
        )
        mock_get_product_member.assert_called_with(self.product_1, self.user_internal)

    @patch("application.core.api.permissions.get_product_member")
    def test_has_object_permission_delete_owner_not_owner(
        self, mock_get_product_member
    ):
        mock_get_product_member.return_value = Product_Member(
            product=self.product_1, user=self.user_internal, role=Roles.Maintainer
        )

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(
            product=self.product_1, user=self.user_external, role=Roles.Owner
        )

        user_has_product_permission = UserHasProductMemberPermission()

        self.assertFalse(
            user_has_product_permission.has_object_permission(
                request=request, view=None, obj=product_member
            )
        )
        mock_get_product_member.assert_called_with(self.product_1, self.user_internal)

    @patch("application.core.api.permissions.get_product_member")
    @patch("application.core.api.permissions.check_object_permission")
    def test_has_object_permission_delete_owner_success(
        self, mock_check, mock_get_product_member
    ):
        mock_check.return_value = True
        mock_get_product_member.return_value = Product_Member(
            product=self.product_1, user=self.user_internal, role=Roles.Owner
        )

        request = HttpRequest()
        request.user = self.user_internal
        request.method = "DELETE"

        product_member = Product_Member(
            product=self.product_1, user=self.user_external, role=Roles.Owner
        )

        user_has_product_permission = UserHasProductMemberPermission()

        self.assertTrue(
            user_has_product_permission.has_object_permission(
                request=request, view=None, obj=product_member
            )
        )
        mock_get_product_member.assert_called_with(self.product_1, self.user_internal)
        mock_check.assert_called_once()
