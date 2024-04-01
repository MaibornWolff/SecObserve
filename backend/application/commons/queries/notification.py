from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet

from application.commons.models import Notification
from application.commons.services.global_request import get_current_user
from application.core.models import Product_Authorization_Group_Member, Product_Member


def get_notifications() -> QuerySet[Notification]:
    user = get_current_user()

    if user is None:
        return Notification.objects.none()

    notifications = Notification.objects.all()

    if not user.is_superuser:
        product_members = Product_Member.objects.filter(
            product=OuterRef("product_id"), user=user
        )
        product_group_members = Product_Member.objects.filter(
            product=OuterRef("product__product_group"), user=user
        )

        product_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("product_id"),
                authorization_group__users=user,
            )
        )

        product_group_authorization_group_members = (
            Product_Authorization_Group_Member.objects.filter(
                product=OuterRef("product__product_group"),
                authorization_group__users=user,
            )
        )

        notifications = notifications.annotate(
            product__member=Exists(product_members),
            product__product_group__member=Exists(product_group_members),
            authorization_group_member=Exists(product_authorization_group_members),
            product_group_authorization_group_member=Exists(
                product_group_authorization_group_members
            ),
        )

        notifications = notifications.filter(
            (
                Q(product__member=True)
                | Q(product__product_group__member=True)
                | Q(authorization_group_member=True)
                | Q(product_group_authorization_group_member=True)
            )
            & (Q(type=Notification.TYPE_SECURITY_GATE) | Q(type=Notification.TYPE_TASK))
        )

    return notifications
