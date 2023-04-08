from rest_framework.exceptions import PermissionDenied

from application.access_control.models import User
from application.access_control.services.roles_permissions import (
    Permissions,
    Roles,
    get_roles_with_permissions,
)
from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Product, Product_Member
from application.core.queries.product import get_product_member
from application.import_observations.models import Api_Configuration
from application.rules.models import Rule


def user_has_permission(obj, permission: int, user: User = None) -> bool:
    if user is None:
        user = get_current_user()

    if user is None:
        return False

    if user.is_superuser:
        return True

    if isinstance(obj, Product):
        # Check if the user has a role for the product with the requested permissions
        member = get_product_member(obj, user)
        if member is not None and role_has_permission(member.role, permission):
            return True
        else:
            return False
    elif (
        isinstance(obj, Product_Member)
        and permission in Permissions.get_product_member_permissions()
    ):
        return user_has_permission(obj.product, permission, user)
    elif (
        isinstance(obj, Rule)
        and permission in Permissions.get_product_rule_permissions()
    ):
        if obj.product:
            return user_has_permission(obj.product, permission, user)
        else:
            raise NoAuthorizationImplementedError(
                "No authorization implemented for General Rules"
            )
    elif (
        isinstance(obj, Observation)
        and permission in Permissions.get_observation_permissions()
    ):
        return user_has_permission(obj.product, permission, user)
    elif (
        isinstance(obj, Api_Configuration)
        and permission in Permissions.get_api_configuration_permissions()
    ):
        return user_has_permission(obj.product, permission, user)
    else:
        raise NoAuthorizationImplementedError(
            f"No authorization implemented for class {type(obj).__name__} and permission {permission}"
        )


def user_has_permission_or_403(obj, permission: int, user: User = None) -> None:
    if not user_has_permission(obj, permission, user):
        raise PermissionDenied()


def role_has_permission(role: int, permission: int) -> bool:
    if not Permissions.has_value(permission):
        raise PermissionDoesNotExistError(f"Permission {permission} does not exist")

    if not Roles.has_value(role):
        raise RoleDoesNotExistError(f"Role {role} does not exist")

    roles = get_roles_with_permissions()
    permissions = roles.get(role)
    if not permissions:
        return False
    return permission in permissions


def get_user_permissions(user: User = None) -> list[Permissions]:
    if not user:
        user = get_current_user()

    permissions = []

    if user and not user.is_external:
        permissions.append(Permissions.Product_Create)

    return permissions


class NoAuthorizationImplementedError(Exception):
    def __init__(self, message):
        self.message = message


class PermissionDoesNotExistError(Exception):
    def __init__(self, message):
        self.message = message


class RoleDoesNotExistError(Exception):
    def __init__(self, message):
        self.message = message
