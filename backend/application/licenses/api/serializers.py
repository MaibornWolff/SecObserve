from typing import Optional

from packageurl import PackageURL
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from application.access_control.api.serializers import UserListSerializer
from application.commons.services.global_request import get_current_user
from application.core.types import PURL_Type
from application.licenses.models import (
    License,
    License_Component,
    License_Group,
    License_Group_Member,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license_group_member import get_license_group_member
from application.licenses.queries.license_policy_member import get_license_policy_member
from application.licenses.services.license_policy import get_ignore_component_type_list


class LicenseSerializer(ModelSerializer):
    is_in_license_group = SerializerMethodField()

    class Meta:
        model = License
        fields = "__all__"

    def get_is_in_license_group(self, obj: License) -> bool:
        return License_Group.objects.filter(licenses=obj).exists()


class LicenseComponentSerializer(ModelSerializer):
    license_data = LicenseSerializer(
        source="license",
        read_only=True,
    )
    purl_namespace = SerializerMethodField()
    branch_name = SerializerMethodField()
    license_policy_name = SerializerMethodField()
    license_policy_id = SerializerMethodField()

    class Meta:
        model = License_Component
        fields = "__all__"

    def get_purl_namespace(self, obj: License_Component) -> Optional[str]:
        if obj.purl:
            purl = PackageURL.from_string(obj.purl)
            return purl.namespace

        return ""

    def get_branch_name(self, obj: License_Component) -> str:
        if obj.branch:
            return obj.branch.name

        return ""

    def get_license_policy_name(self, obj: License_Component) -> str:
        if obj.product.license_policy:
            return obj.product.license_policy.name

        if obj.product.product_group and obj.product.product_group.license_policy:
            return obj.product.product_group.license_policy.name

        return ""

    def get_license_policy_id(self, obj: License_Component) -> int:
        if obj.product.license_policy:
            return obj.product.license_policy.pk

        if obj.product.product_group and obj.product.product_group.license_policy:
            return obj.product.product_group.license_policy.pk

        return 0


class LicenseComponentBulkDeleteSerializer(Serializer):
    components = ListField(
        child=IntegerField(min_value=1), min_length=0, max_length=100, required=True
    )


class LicenseGroupSerializer(ModelSerializer):
    is_manager = SerializerMethodField()

    class Meta:
        model = License_Group
        exclude = ["licenses"]

    def get_is_manager(self, obj: License_Group) -> bool:
        user = get_current_user()
        return License_Group_Member.objects.filter(
            license_group=obj, user=user, is_manager=True
        ).exists()


class LicenseGroupLicenseAddRemoveSerializer(Serializer):
    license = IntegerField(min_value=1, required=True)


class LicenseGroupMemberSerializer(ModelSerializer):
    license_group_data = LicenseGroupSerializer(
        source="license_group",
        read_only=True,
    )
    user_data = UserListSerializer(source="user", read_only=True)

    class Meta:
        model = License_Group_Member
        fields = "__all__"

    def validate(self, attrs: dict):
        self.instance: License_Group_Member
        data_license_group: Optional[License_Group] = attrs.get("license_group")
        data_user = attrs.get("user")

        if self.instance is not None and (
            (data_license_group and data_license_group != self.instance.license_group)
            or (data_user and data_user != self.instance.user)
        ):
            raise ValidationError("License group and user cannot be changed")

        if self.instance is None:
            license_group_member = get_license_group_member(
                data_license_group, data_user
            )
            if license_group_member:
                raise ValidationError(
                    f"License group member {data_license_group} / {data_user} already exists"
                )

        return attrs


class LicenseGroupCopySerializer(Serializer):
    name = CharField(max_length=255, required=True)


class LicensePolicySerializer(ModelSerializer):
    is_manager = SerializerMethodField()
    has_products = SerializerMethodField()

    class Meta:
        model = License_Policy
        fields = "__all__"

    def validate_ignore_component_types(self, value: str) -> str:
        ignore_component_types = get_ignore_component_type_list(value)
        for component_type in ignore_component_types:
            for component_type in ignore_component_types:
                if not PURL_Type.PURL_TYPE_CHOICES.get(component_type):
                    raise ValidationError(f"Invalid component type {component_type}")

        return value

    def get_is_manager(self, obj: License_Policy) -> bool:
        user = get_current_user()
        return License_Policy_Member.objects.filter(
            license_policy=obj, user=user, is_manager=True
        ).exists()

    def get_has_products(self, obj: License_Policy) -> bool:
        return obj.product.exists()


class LicensePolicyItemSerializer(ModelSerializer):
    license_spdx_id = SerializerMethodField()
    license_group_name = SerializerMethodField()
    license_policy_data = LicensePolicySerializer(
        source="license_policy",
        read_only=True,
    )

    class Meta:
        model = License_Policy_Item
        exclude = ["numerical_evaluation_result"]

    def get_license_spdx_id(self, obj: License_Policy_Item) -> str:
        if obj.license:
            return obj.license.spdx_id

        return ""

    def get_license_group_name(self, obj: License_Policy_Item) -> str:
        if obj.license_group:
            return obj.license_group.name

        return ""

    def validate(self, attrs: dict):
        self.instance: License_Policy_Item
        data_license_group = attrs.get("license_group")
        data_license = attrs.get("license")
        data_unknown_license = attrs.get("unknown_license", "")

        if self.instance:
            self.instance.license_group = data_license_group
            self.instance.license = data_license
            self.instance.unknown_license = data_unknown_license
            num_fields = (
                bool(self.instance.license_group)
                + bool(self.instance.license)
                + bool(self.instance.unknown_license)
            )
            try:
                item = License_Policy_Item.objects.get(
                    license_policy=self.instance.license_policy,
                    license_group=self.instance.license_group,
                    license=self.instance.license,
                    unknown_license=self.instance.unknown_license,
                )
                if item.pk != self.instance.pk:
                    raise ValidationError("License policy item already exists")
            except License_Policy_Item.DoesNotExist:
                pass
        else:
            num_fields = (
                bool(data_license_group)
                + bool(data_license)
                + bool(data_unknown_license)
            )
            try:
                License_Policy_Item.objects.get(
                    license_policy=attrs.get("license_policy"),
                    license_group=data_license_group,
                    license=data_license,
                    unknown_license=data_unknown_license,
                )
                raise ValidationError("License policy item already exists")
            except License_Policy_Item.DoesNotExist:
                pass

        if num_fields == 0:
            raise ValidationError(
                "One of license group, license or unknown license must be set"
            )
        if num_fields > 1:
            raise ValidationError(
                "Only one of license group, license or unknown license must be set"
            )
        return attrs


class LicensePolicyMemberSerializer(ModelSerializer):
    license_policy_data = LicensePolicySerializer(
        source="license_policy",
        read_only=True,
    )
    user_data = UserListSerializer(source="user", read_only=True)

    class Meta:
        model = License_Policy_Member
        fields = "__all__"

    def validate(self, attrs: dict):
        self.instance: License_Policy_Member
        data_license_policy: Optional[License_Policy] = attrs.get("license_policy")
        data_user = attrs.get("user")

        if self.instance is not None and (
            (
                data_license_policy
                and data_license_policy != self.instance.license_policy
            )
            or (data_user and data_user != self.instance.user)
        ):
            raise ValidationError("License policy and user cannot be changed")

        if self.instance is None:
            license_group_member = get_license_policy_member(
                data_license_policy, data_user
            )
            if license_group_member:
                raise ValidationError(
                    f"License policy member {data_license_policy} / {data_user} already exists"
                )

        return attrs


class LicensePolicyCopySerializer(Serializer):
    name = CharField(max_length=255, required=True)
