from django.core.validators import MinValueValidator
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.access_control.models import Authorization_Group, User
from application.access_control.services.authorization import get_user_permissions
from application.access_control.services.roles_permissions import Permissions, Roles


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
            "setting_list_size",
            "permissions",
            "setting_list_properties",
        ]

    def get_permissions(self, obj) -> list[Permissions]:
        return get_user_permissions(obj)


class AuthorizationGroupSerializer(ModelSerializer):
    class Meta:
        model = Authorization_Group
        fields = "__all__"


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "setting_theme",
            "setting_list_size",
            "setting_list_properties",
        ]


class AuthenticationRequestSerializer(Serializer):
    username = CharField(max_length=150, required=True)
    password = CharField(max_length=128, required=True)


class AuthenticationResponseSerializer(Serializer):
    jwt = CharField()
    user = UserSerializer()


class ProductApiTokenSerializer(Serializer):
    id = IntegerField(validators=[MinValueValidator(0)])
    role = ChoiceField(choices=Roles)


class CreateApiTokenResponseSerializer(Serializer):
    token = CharField()
