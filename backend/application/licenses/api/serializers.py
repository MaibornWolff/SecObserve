from typing import Optional

from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from application.access_control.api.serializers import UserListSerializer
from application.commons.services.global_request import get_current_user
from application.licenses.models import (
    License,
    License_Group,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license_policy_member import get_license_policy_member


class LicenseSerializer(ModelSerializer):
    is_in_license_group = SerializerMethodField()

    class Meta:
        model = License
        fields = "__all__"

    def get_is_in_license_group(self, obj: License) -> bool:
        return License_Group.objects.filter(licenses=obj).exists()


class LicenseGroupSerializer(ModelSerializer):
    class Meta:
        model = License_Group
        exclude = ["licenses"]


class LicensePolicySerializer(ModelSerializer):
    is_manager = SerializerMethodField()

    class Meta:
        model = License_Policy
        fields = "__all__"

    def get_is_manager(self, obj: License_Policy) -> bool:
        user = get_current_user()
        return License_Policy_Member.objects.filter(
            license_policy=obj, user=user, is_manager=True
        ).exists()


class LicensePolicyItemSerializer(ModelSerializer):
    license_spdx_id = SerializerMethodField()
    license_group_name = SerializerMethodField()
    license_policy_data = LicensePolicySerializer(
        source="license_policy",
        read_only=True,
    )

    class Meta:
        model = License_Policy_Item
        fields = "__all__"

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
        data_unknown_license = attrs.get("unknown_license")

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
            raise ValidationError("Authorization group and user cannot be changed")

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
    license_policy = IntegerField(min_value=1, required=True)
    name = CharField(max_length=255, required=True)
