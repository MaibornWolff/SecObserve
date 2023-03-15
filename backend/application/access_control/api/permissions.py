from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError

from application.access_control.services.authorization import user_has_permission


def check_post_permission(request, post_model, post_foreign_key, post_permission):
    if request.method == "POST":
        if request.data.get(post_foreign_key) is None:
            raise ParseError(
                f"Unable to check for permissions: Attribute '{post_foreign_key}' is required"
            )
        object = get_object_or_404(post_model, pk=request.data.get(post_foreign_key))
        return user_has_permission(object, post_permission)
    else:
        return True


def check_object_permission(
    request,
    object,
    get_permission,
    put_permission,
    delete_permission,
    post_permission=None,
):
    if request.method == "GET":
        return user_has_permission(object, get_permission)
    elif request.method == "PUT" or request.method == "PATCH":
        return user_has_permission(object, put_permission)
    elif request.method == "DELETE":
        return user_has_permission(object, delete_permission)
    elif request.method == "POST":
        return user_has_permission(object, post_permission)
    else:
        return False
