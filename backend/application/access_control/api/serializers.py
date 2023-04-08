from rest_framework.serializers import (
    CharField,
    Serializer,
    ModelSerializer,
    SerializerMethodField,
)
from application.access_control.models import User
from application.access_control.services.authorization import get_user_permissions
from application.access_control.services.roles_permissions import Permissions


class UserSerializer(ModelSerializer):
    permissions = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "is_active",
            "is_superuser",
            "is_external",
            "setting_theme",
            "permissions",
        ]

    def get_permissions(self, obj) -> list[Permissions]:
        return get_user_permissions(obj)


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "setting_theme",
        ]


class AuthenticationRequestSerializer(Serializer):
    username = CharField(max_length=150, required=True)
    password = CharField(max_length=128, required=True)


class AuthenticationResponseSerializer(Serializer):
    jwt = CharField()
    user = UserSerializer()


class CreateAPITokenResponseSerializer(Serializer):
    token = CharField()
