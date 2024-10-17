from django.db.models.query import QuerySet

from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Policy_Item
from application.licenses.queries.license_policy import get_license_policys


def get_license_policy_items() -> QuerySet[License_Policy_Item]:
    user = get_current_user()

    if user is None:
        return License_Policy_Item.objects.none()

    license_policy_items = License_Policy_Item.objects.all()

    if user.is_superuser:
        return license_policy_items

    license_policys = get_license_policys()
    return license_policy_items.filter(license_policy__in=license_policys)
