from typing import Optional

from rest_framework.exceptions import PermissionDenied

from application.access_control.models import User
from application.access_control.services.roles_permissions import (
    Permissions,
    Roles,
    get_roles_with_permissions,
)
from application.commons.services.global_request import get_current_user
from application.core.models import (
    Branch,
    Observation,
    Observation_Log,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
    Service,
)
from application.core.queries.product_member import (
    get_highest_role_of_product_authorization_group_members_for_user,
    get_product_member,
)
from application.import_observations.models import (
    Api_Configuration,
    Vulnerability_Check,
)
from application.rules.models import Rule
from application.vex.models import VEX_Base


def user_has_permission(  # pylint: disable=too-many-return-statements,too-many-branches
    obj, permission: int, user: User = None
) -> bool:
    # There are a lot of different objects that need to be checked for permissions.
    # Refactoring it wouldn't make it more readable.

    if user is None:
        user = get_current_user()

    if user is None:
        return False

    if user.is_superuser:
        return True

    if (
        isinstance(obj, Product)
        and not obj.is_product_group
        and permission not in Permissions.get_product_group_permissions()
    ):
        role = get_highest_user_role(obj, user)
        return bool(role and role_has_permission(role, permission))

    if isinstance(obj, Product) and obj.is_product_group:
        role = get_highest_user_role(obj, user)
        return bool(role and role_has_permission(role, permission))

    if (
        isinstance(obj, Product_Member)
        and permission in Permissions.get_product_member_permissions()
    ):
        return user_has_permission(obj.product, permission, user)

    if (
        isinstance(obj, Product_Authorization_Group_Member)
        and permission
        in Permissions.get_product_authorization_group_member_permissions()
    ):
        return user_has_permission(obj.product, permission, user)

    if (
        isinstance(obj, Rule)
        and permission in Permissions.get_product_rule_permissions()
    ):
        if not obj.product:
            raise NoAuthorizationImplementedError(
                "No authorization implemented for General Rules"
            )

        return user_has_permission(obj.product, permission, user)

    if isinstance(obj, Branch) and permission in Permissions.get_branch_permissions():
        return user_has_permission(obj.product, permission, user)

    if isinstance(obj, Service) and permission in Permissions.get_service_permissions():
        return user_has_permission(obj.product, permission, user)

    if (
        isinstance(obj, Observation)
        and permission in Permissions.get_observation_permissions()
    ):
        return user_has_permission(obj.product, permission, user)

    if (
        isinstance(obj, Observation_Log)
        and permission in Permissions.get_observation_log_permissions()
    ):
        return user_has_permission(obj.observation.product, permission, user)

    if (
        isinstance(obj, Api_Configuration)
        and permission in Permissions.get_api_configuration_permissions()
    ):
        return user_has_permission(obj.product, permission, user)

    if isinstance(obj, VEX_Base) and permission in Permissions.get_vex_permissions():
        if user == obj.user:
            return True
        if obj.product:
            return user_has_permission(obj.product, permission, user)
        return False

    if (
        isinstance(obj, Vulnerability_Check)
        and permission in Permissions.get_vulnerability_check_permissions()
    ):
        return user_has_permission(obj.product, permission, user)

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


def get_highest_user_role(product: Product, user: User = None) -> Optional[int]:
    if user is None:
        user = get_current_user()

    if not user:
        return None

    if user.is_superuser:
        return Roles.Owner

    user_member = get_product_member(product, user)
    user_product_role = user_member.role if user_member else 0

    user_product_group_role = 0
    if product.product_group:
        user_product_group_member = get_product_member(product.product_group, user)
        user_product_group_role = (
            user_product_group_member.role if user_product_group_member else 0
        )

    authorization_group_role = (
        get_highest_role_of_product_authorization_group_members_for_user(product, user)
    )
    highest_role = max(
        user_product_role, user_product_group_role, authorization_group_role
    )

    if highest_role:
        return highest_role

    return None


def get_user_permissions(user: User = None) -> list[Permissions]:
    if not user:
        user = get_current_user()

    permissions = []

    if user and not user.is_external:
        permissions.append(Permissions.Product_Create)
        permissions.append(Permissions.Product_Group_Create)

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
