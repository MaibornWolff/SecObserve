from typing import Any, Optional

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from application.access_control.models import (
    API_Token,
    Authorization_Group,
    Authorization_Group_Member,
    User,
)
from application.access_control.queries.authorization_group_member import (
    get_authorization_group_member,
)
from application.access_control.services.authorization import get_user_permissions
from application.access_control.services.current_user import get_current_user
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Product_Authorization_Group_Member, Product_Member


class NestedAuthorizationGroupSerializer(ModelSerializer):
    class Meta:
        model = Authorization_Group
        exclude = ["users"]


class UserListSerializer(ModelSerializer):
    full_name = SerializerMethodField()
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

    def to_representation(self, instance: User) -> dict[str, Any]:
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

    def get_full_name(self, obj: User) -> str:
        if not obj.is_active:
            return f"{obj.full_name} (inactive)"

        return obj.full_name

    def get_permissions(self, obj: User) -> list[Permissions]:
        return get_user_permissions(obj)

    def get_has_password(self, obj: User) -> bool:
        return bool(obj.password and obj.password != "" and obj.has_usable_password())  # nosec B105
        # eliminate false positive, password is not hardcoded


class UserSerializer(UserListSerializer):
    full_name = SerializerMethodField()
    has_authorization_groups = SerializerMethodField()
    has_product_group_members = SerializerMethodField()
    has_product_members = SerializerMethodField()

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
            "has_authorization_groups",
            "has_product_group_members",
            "has_product_members",
        ]

    def to_representation(self, instance: User) -> dict[str, Any]:
        data = super().to_representation(instance)

        user = get_current_user()
        if user and not user.is_superuser and not user.pk == instance.pk:
            data.pop("has_authorization_groups")
            data.pop("has_product_group_members")
            data.pop("has_product_members")

        return data

    def get_full_name(self, obj: User) -> str:
        return obj.full_name

    def get_has_authorization_groups(self, obj: User) -> bool:
        return Authorization_Group_Member.objects.filter(user=obj).exists()

    def get_has_product_group_members(self, obj: User) -> bool:
        return Product_Member.objects.filter(user=obj, product__is_product_group=True).exists()

    def get_has_product_members(self, obj: User) -> bool:
        return Product_Member.objects.filter(user=obj, product__is_product_group=False).exists()


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
    has_product_group_members = SerializerMethodField()
    has_product_members = SerializerMethodField()
    has_users = SerializerMethodField()
    is_manager = SerializerMethodField()

    class Meta:
        model = Authorization_Group
        exclude = ["users"]

    def get_has_product_group_members(self, obj: Authorization_Group) -> bool:
        return Product_Authorization_Group_Member.objects.filter(
            authorization_group=obj, product__is_product_group=True
        ).exists()

    def get_has_product_members(self, obj: Authorization_Group) -> bool:
        return Product_Authorization_Group_Member.objects.filter(
            authorization_group=obj, product__is_product_group=False
        ).exists()

    def get_has_users(self, obj: Authorization_Group) -> bool:
        return Authorization_Group_Member.objects.filter(authorization_group=obj).exists()

    def get_is_manager(self, obj: Authorization_Group) -> bool:
        user = get_current_user()
        return Authorization_Group_Member.objects.filter(authorization_group=obj, user=user, is_manager=True).exists()


class AuthorizationGroupListSerializer(ModelSerializer):
    class Meta:
        model = Authorization_Group
        exclude = ["users"]


class AuthorizationGroupMemberSerializer(ModelSerializer):
    authorization_group_data = AuthorizationGroupListSerializer(
        source="authorization_group",
        read_only=True,
    )
    user_data = UserListSerializer(source="user", read_only=True)

    class Meta:
        model = Authorization_Group_Member
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:
        self.instance: Authorization_Group_Member
        data_authorization_group: Optional[Authorization_Group] = attrs.get("authorization_group")
        data_user = attrs.get("user")

        if self.instance is not None and (
            (data_authorization_group and data_authorization_group != self.instance.authorization_group)
            or (data_user and data_user != self.instance.user)
        ):
            raise ValidationError("Authorization group and user cannot be changed")

        if self.instance is None:
            if data_authorization_group is None:
                raise ValidationError("Authorization group is required")
            if data_user is None:
                raise ValidationError("User is required")

            authorization_group_member = get_authorization_group_member(data_authorization_group, data_user)
            if authorization_group_member:
                raise ValidationError(
                    f"Authorization group member {data_authorization_group} / {data_user} already exists"
                )

        return attrs


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
    role = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


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
        product_member = Product_Member.objects.filter(user=obj.user, product__is_product_group=False).first()
        if product_member:
            return product_member.product.pk
        return None

    def get_product_group(self, obj: API_Token) -> Optional[int]:
        product_member = Product_Member.objects.filter(user=obj.user, product__is_product_group=True).first()
        if product_member:
            return product_member.product.pk
        return None


class CreateApiTokenResponseSerializer(Serializer):
    token = CharField()
