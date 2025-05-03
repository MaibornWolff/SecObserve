from typing import Optional

from django.contrib.auth.models import AnonymousUser

from application.access_control.models import User
from application.commons.services.global_request import get_current_request


def get_current_user() -> Optional[User]:
    request = get_current_request()
    if request and request.user and not isinstance(request.user, AnonymousUser):
        return request.user

    return None
