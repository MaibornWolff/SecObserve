from unittest.mock import patch

from django.http import Http404, HttpRequest
from rest_framework.exceptions import ParseError

from application.authorization.api.permissions_base import (
    check_object_permission,
    check_post_permission,
)
from application.authorization.services.roles_permissions import Permissions
from application.core.models import Product
from unittests.base_test_case import BaseTestCase


class TestPermissions(BaseTestCase):
    # --- check_post_permission ---

    def test_check_post_permission_not_post(self):
        request = HttpRequest()
        request.method = "GET"
        self.assertTrue(check_post_permission(request, None, None, None))

    def test_check_post_permission_no_foreign_key(self):
        request = HttpRequest()
        request.method = "POST"
        request.data = {}
        with self.assertRaises(ParseError) as e:
            check_post_permission(request, None, "product", None)

        self.assertEqual(
            "Unable to check for permissions: Attribute 'product' is required",
            str(e.exception),
        )

    @patch("application.authorization.api.permissions_base.get_object_or_404")
    def test_check_post_permission_foreign_key_not_found(self, mock):
        mock.side_effect = Http404()
        request = HttpRequest()
        request.method = "POST"
        request.data = {"product": 1}
        with self.assertRaises(Http404):
            check_post_permission(request, Product, "product", None)

        mock.assert_called_with(Product, pk=1)

    @patch("application.authorization.api.permissions_base.get_object_or_404")
    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_post_permission_successful(self, permission_mock, get_mock):
        get_mock.return_value = self.product_1
        permission_mock.return_value = True
        request = HttpRequest()
        request.method = "POST"
        request.data = {"product": 1}

        self.assertTrue(check_post_permission(request, Product, "product", Permissions.Product_Member_Create))
        get_mock.assert_called_with(Product, pk=1)
        permission_mock.assert_called_with(self.product_1, Permissions.Product_Member_Create)

    # --- check_object_permission ---

    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_object_permission_get(self, mock):
        mock.return_value = True
        request = HttpRequest()
        request.method = "GET"

        self.assertTrue(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
        mock.assert_called_with(self.product_1, Permissions.Product_View)

    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_object_permission_put(self, mock):
        mock.return_value = True
        request = HttpRequest()
        request.method = "PUT"

        self.assertTrue(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
        mock.assert_called_with(self.product_1, Permissions.Product_Edit)

    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_object_permission_patch(self, mock):
        mock.return_value = True
        request = HttpRequest()
        request.method = "PATCH"

        self.assertTrue(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
        mock.assert_called_with(self.product_1, Permissions.Product_Edit)

    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_object_permission_delete(self, mock):
        mock.return_value = True
        request = HttpRequest()
        request.method = "DELETE"

        self.assertTrue(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
        mock.assert_called_with(self.product_1, Permissions.Product_Delete)

    @patch("application.authorization.api.permissions_base.user_has_permission")
    def test_check_object_permission_post(self, mock):
        mock.return_value = True
        request = HttpRequest()
        request.method = "POST"

        self.assertTrue(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
        mock.assert_called_with(self.product_1, Permissions.Product_Create)

    def test_check_object_permission_other(self):
        request = HttpRequest()
        request.method = "OTHER"

        self.assertFalse(
            check_object_permission(
                request=request,
                object_to_check=self.product_1,
                get_permission=Permissions.Product_View,
                put_permission=Permissions.Product_Edit,
                delete_permission=Permissions.Product_Delete,
                post_permission=Permissions.Product_Create,
            )
        )
