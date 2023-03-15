from unittest.mock import patch

from rest_framework.exceptions import PermissionDenied

from unittests.base_test_case import BaseTestCase
from application.access_control.services.authorization import (
    user_has_permission,
    user_has_permission_or_403,
    get_user_permission,
    role_has_permission,
    PermissionDoesNotExistError,
    RoleDoesNotExistError,
    NoAuthorizationImplementedError,
)
from application.access_control.services.roles_permissions import Permissions, Roles


class TestAuthorization(BaseTestCase):
    # ---------------------------------------------------------------
    # user_has_permission
    # ---------------------------------------------------------------

    @patch("application.access_control.services.authorization.get_current_user")
    def test_user_has_permission_superuser(self, mock):
        mock.return_value = self.user_admin
        self.assertTrue(user_has_permission(None, Permissions.Observation_Delete))

    # --- Product ---

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_product_no_member(self, mock):
        mock.return_value = None
        self.assertFalse(
            user_has_permission(
                self.product_1, Permissions.Product_View, self.user_external
            )
        )
        mock.assert_called_with(self.product_1, self.user_external)

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_product_no_permissions(self, mock):
        mock.return_value = self.product_member_1
        self.assertFalse(
            user_has_permission(
                self.product_1, Permissions.Product_Edit, self.user_internal
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_product_successful(self, mock):
        mock.return_value = self.product_member_1
        self.assertTrue(
            user_has_permission(
                self.product_1,
                Permissions.Product_Import_Observations,
                self.user_internal,
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    # --- Product_Member ---

    def test_user_has_permission_product_member_wrong_permission(self):
        with self.assertRaises(NoAuthorizationImplementedError) as e:
            user_has_permission(
                self.product_member_1, Permissions.Product_Edit, self.user_internal
            )
        self.assertEqual(
            "No authorization implemented for class Product_Member and permission 1102",
            str(e.exception),
        )

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_product_member_correct_permission(self, mock):
        mock.return_value = self.product_member_1
        self.assertFalse(
            user_has_permission(
                self.product_member_1,
                Permissions.Product_Member_Edit,
                self.user_internal,
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    # --- Rule ---

    def test_user_has_permission_rule_wrong_permission(self):
        with self.assertRaises(NoAuthorizationImplementedError) as e:
            user_has_permission(
                self.product_rule_1, Permissions.Product_Edit, self.user_internal
            )
        self.assertEqual(
            "No authorization implemented for class Rule and permission 1102",
            str(e.exception),
        )

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_rule_correct_permission(self, mock):
        mock.return_value = self.product_member_1
        self.assertFalse(
            user_has_permission(
                self.product_rule_1, Permissions.Product_Rule_Edit, self.user_internal
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    def test_user_has_permission_rule_general_rule(self):
        with self.assertRaises(NoAuthorizationImplementedError) as e:
            user_has_permission(
                self.general_rule, Permissions.Product_Rule_View, self.user_internal
            )
        self.assertEqual(
            "No authorization implemented for General Rules", str(e.exception)
        )

    # --- Observation ---

    def test_user_has_permission_observation_wrong_permission(self):
        with self.assertRaises(NoAuthorizationImplementedError) as e:
            user_has_permission(
                self.observation_1, Permissions.Product_Edit, self.user_internal
            )
        self.assertEqual(
            "No authorization implemented for class Observation and permission 1102",
            str(e.exception),
        )

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_observation_correct_permission(self, mock):
        mock.return_value = self.product_member_1
        self.assertFalse(
            user_has_permission(
                self.observation_1, Permissions.Observation_Delete, self.user_internal
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    # --- Api_Configuration ---

    def test_user_has_permission_api_configuration_wrong_permission(self):
        with self.assertRaises(NoAuthorizationImplementedError) as e:
            user_has_permission(
                self.api_configuration_1, Permissions.Product_Edit, self.user_internal
            )
        self.assertEqual(
            "No authorization implemented for class Api_Configuration and permission 1102",
            str(e.exception),
        )

    @patch("application.access_control.services.authorization.get_product_member")
    def test_user_has_permission_api_configuration_correct_permission(self, mock):
        mock.return_value = self.product_member_1
        self.assertFalse(
            user_has_permission(
                self.api_configuration_1,
                Permissions.Api_Configuration_Edit,
                self.user_internal,
            )
        )
        mock.assert_called_with(self.product_1, self.user_internal)

    # ---------------------------------------------------------------
    # user_has_permission_or_403
    # ---------------------------------------------------------------

    @patch("application.access_control.services.authorization.user_has_permission")
    def test_user_has_permission_or_403_permission_denied(self, mock):
        mock.return_value = False
        with self.assertRaises(PermissionDenied):
            user_has_permission_or_403(None, Permissions.Product_Edit)

    @patch("application.access_control.services.authorization.user_has_permission")
    def test_user_has_permission_or_403_successful(self, mock):
        mock.return_value = True
        user_has_permission_or_403(None, Permissions.Product_Edit)

    # ---------------------------------------------------------------
    # role_has_permission
    # ---------------------------------------------------------------

    def test_role_has_permission_wrong_role(self):
        with self.assertRaises(RoleDoesNotExistError) as e:
            role_has_permission(99999, Permissions.Product_Edit)
        self.assertEqual("Role 99999 does not exist", str(e.exception))

    def test_role_has_permission_wrong_permission(self):
        with self.assertRaises(PermissionDoesNotExistError) as e:
            role_has_permission(Roles.Reader, 99999)
        self.assertEqual("Permission 99999 does not exist", str(e.exception))

    @patch(
        "application.access_control.services.authorization.get_roles_with_permissions"
    )
    def test_role_has_permission_no_permission(self, mock):
        mock.return_value = {Roles.Reader: {}}
        self.assertFalse(
            role_has_permission(Roles.Reader, Permissions.Observation_Delete)
        )

    def test_role_has_permission_not_permitted(self):
        self.assertFalse(
            role_has_permission(Roles.Maintainer, Permissions.Observation_Delete)
        )

    def test_role_has_permission_successful(self):
        self.assertTrue(
            role_has_permission(Roles.Owner, Permissions.Observation_Delete)
        )

    # ---------------------------------------------------------------
    # get_user_permission
    # ---------------------------------------------------------------

    def test_get_user_permission_internal(self):
        permissions = get_user_permission(self.user_internal)
        self.assertEqual([Permissions.Product_Create], permissions)

    @patch("application.access_control.services.authorization.get_current_user")
    def test_get_user_permission_external(self, mock):
        mock.return_value = self.user_external

        permissions = get_user_permission()
        self.assertEqual([], permissions)
