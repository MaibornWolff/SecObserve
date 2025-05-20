from django.db.models.query import QuerySet

from application.access_control.services.current_user import get_current_user
from application.licenses.models import License_Policy_Item
from application.licenses.queries.license_policy import get_license_policies


def get_license_policy_items() -> QuerySet[License_Policy_Item]:
    user = get_current_user()

    if user is None:
        return License_Policy_Item.objects.none()

    license_policy_items = License_Policy_Item.objects.all().order_by("id")

    if user.is_superuser:
        return license_policy_items

    license_policies = get_license_policies()
    return license_policy_items.filter(license_policy__in=license_policies)
