from typing import Optional

from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.commons.models import Notification, Notification_Viewed, Settings
from application.commons.services.global_request import get_current_user


class VersionSerializer(Serializer):
    version = CharField(max_length=200)


class StatusSettingsSerializer(Serializer):
    features = ListField(child=CharField(), min_length=0, max_length=200, required=True)
    risk_acceptance_expiry_days = IntegerField()


class SettingsSerializer(ModelSerializer):
    id = SerializerMethodField()

    class Meta:
        model = Settings
        fields = "__all__"

    def get_id(self, obj: Settings) -> int:  # pylint: disable=unused-argument
        # obj is needed for the signature but we don't need it
        # The id is hardcoded to 1 because there is only one instance of the Settings model
        return 1


class NotificationSerializer(ModelSerializer):
    message = SerializerMethodField()
    product_name = SerializerMethodField()
    observation_title = SerializerMethodField()
    user_full_name = SerializerMethodField()
    new_viewed = SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_message(self, obj: Notification) -> Optional[str]:
        if not obj.message:
            return obj.message

        user = get_current_user()
        if user and user.is_superuser:
            return obj.message

        return "..."

    def get_product_name(self, obj: Notification) -> Optional[str]:
        if obj.product:
            return obj.product.name

        if obj.observation:
            return obj.observation.product.name

        return None

    def get_observation_title(self, obj: Notification) -> Optional[str]:
        if obj.observation:
            return obj.observation.title

        return None

    def get_user_full_name(self, obj: Notification) -> Optional[str]:
        if obj.user:
            return obj.user.full_name

        return None

    def get_new_viewed(self, obj: Notification) -> str:
        user = get_current_user()
        if user:
            notification_viewed = Notification_Viewed.objects.filter(
                notification=obj, user=user
            ).first()
            if notification_viewed:
                return "Viewed"
        return "New"


class NotificationBulkSerializer(Serializer):
    notifications = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=250, required=True
    )
