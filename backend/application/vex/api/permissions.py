from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from application.access_control.api.permissions_base import check_object_permission
from application.access_control.services.roles_permissions import Permissions
from application.vex.models import CSAF, OpenVEX


class UserHasVEXPermission(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: CSAF | OpenVEX) -> bool:
        return check_object_permission(
            request=request,
            object_to_check=obj,
            get_permission=Permissions.VEX_View,
            put_permission=Permissions.VEX_Edit,
            delete_permission=Permissions.VEX_Delete,
        )


class UserHasVEXCounterPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == "GET":
            return True

        if not request.user:
            return False

        if isinstance(request.user, AnonymousUser):
            return False

        return request.user.is_superuser
