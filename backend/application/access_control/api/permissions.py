from rest_framework.permissions import BasePermission


class UserHasSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method != "GET"
            and request.path != "/api/users/my_settings/"
            and not request.path.endswith("/change_password/")
        ):
            return request.user.is_superuser

        return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method != "GET"
            and request.path != f"/api/users/{obj.pk}/change_password/"
        ):
            return request.user.is_superuser

        return True
