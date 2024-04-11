from typing import Optional

from django.core.validators import MinValueValidator
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.access_control.models import API_Token, Authorization_Group, User
from application.access_control.services.authorization import get_user_permissions
from application.access_control.services.roles_permissions import Permissions, Roles
from application.commons.services.global_request import get_current_user
from application.core.models import Product_Member


class UserSerializer(ModelSerializer):
    permissions = SerializerMethodField()
    has_password = SerializerMethodField()

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
            "oidc_groups_hash",
            "is_oidc_user",
            "date_joined",
            "has_password",
        ]

    def to_representation(self, instance: User):
        data = super().to_representation(instance)

        user = get_current_user()
        if user and not user.is_superuser and not user.pk == instance.pk:
            data.pop("email")
            data.pop("first_name")
            data.pop("last_name")
            data.pop("is_active")
            data.pop("is_superuser")
            data.pop("is_external")
            data.pop("setting_theme")
            data.pop("setting_list_size")
            data.pop("setting_list_properties")
            data.pop("permissions")
            data.pop("oidc_groups_hash")
            data.pop("is_oidc_user")
            data.pop("date_joined")
            data.pop("has_password")

        return data

    def get_permissions(self, obj: User) -> list[Permissions]:
        return get_user_permissions(obj)

    def get_has_password(self, obj: User) -> bool:
        return bool(
            obj.password
            and obj.password != ""  # nosec B105
            and obj.has_usable_password()
        )
        # eliminate false positive, password is not hardcoded


class UserUpdateSerializer(ModelSerializer):
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
        ]


class UserPasswordSerializer(Serializer):
    current_password = CharField(max_length=255, required=False)
    new_password_1 = CharField(max_length=255, required=True)
    new_password_2 = CharField(max_length=255, required=True)


class UserPasswortRulesSerializer(Serializer):
    password_rules = CharField()


class AuthorizationGroupSerializer(ModelSerializer):
    class Meta:
        model = Authorization_Group
        fields = "__all__"


class AuthorizationGroupUserSerializer(Serializer):
    user = IntegerField(validators=[MinValueValidator(0)])


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


class ApiTokenSerializer(ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    product = SerializerMethodField()
    product_group = SerializerMethodField()

    class Meta:
        model = API_Token
        fields = ["id", "name", "product", "product_group"]

    def get_id(self, obj: API_Token) -> int:
        return obj.pk

    def get_name(self, obj: API_Token) -> str:
        return obj.user.username

    def get_product(self, obj: API_Token) -> Optional[int]:
        product_member = Product_Member.objects.filter(
            user=obj.user, product__is_product_group=False
        ).first()
        if product_member:
            return product_member.product.pk
        return None

    def get_product_group(self, obj: API_Token) -> Optional[int]:
        product_member = Product_Member.objects.filter(
            user=obj.user, product__is_product_group=True
        ).first()
        if product_member:
            return product_member.product.pk
        return None


class CreateApiTokenResponseSerializer(Serializer):
    token = CharField()
