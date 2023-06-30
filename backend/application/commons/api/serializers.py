from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.commons.models import Notification


class VersionSerializer(Serializer):
    version = CharField(max_length=200)


class NotificationSerializer(ModelSerializer):
    product_name = SerializerMethodField()
    observation_title = SerializerMethodField()
    user_full_name = SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_product_name(self, obj: Notification):
        if obj.observation:
            return obj.observation.product.name

        return None

    def get_observation_title(self, obj: Notification):
        if obj.observation:
            return obj.observation.title

        return None

    def get_user_full_name(self, obj: Notification):
        if obj.user:
            return obj.user.full_name

        return None


class NotificationBulkSerializer(Serializer):
    notifications = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=100, required=True
    )
