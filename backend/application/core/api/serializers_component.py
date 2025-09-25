from typing import Optional

from packageurl import PackageURL
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from application.core.models import Component


class ComponentSerializer(ModelSerializer):
    product_name = SerializerMethodField()
    product_group_name = SerializerMethodField()
    branch_name = SerializerMethodField()
    component_name_version_type = SerializerMethodField()
    component_purl_namespace = SerializerMethodField()
    origin_service_name = SerializerMethodField()

    def get_product_name(self, obj: Component) -> str:
        return obj.product.name

    def get_product_group_name(self, obj: Component) -> str:
        if obj.product.product_group:
            return obj.product.product_group.name
        return ""

    def get_branch_name(self, obj: Component) -> str:
        if obj.branch:
            return obj.branch.name
        return ""

    def get_component_name_version_type(self, obj: Component) -> str:
        if obj.component_name_version:
            component_name_version_type = obj.component_name_version
            if obj.component_purl_type:
                component_name_version_type += f" ({obj.component_purl_type})"
            return component_name_version_type
        return ""

    def get_component_purl_namespace(self, obj: Component) -> Optional[str]:
        if obj.component_purl:
            try:
                purl = PackageURL.from_string(obj.component_purl)
                return purl.namespace
            except ValueError:
                return ""

        return ""

    def get_origin_service_name(self, obj: Component) -> str:
        if obj.origin_service:
            return obj.origin_service.name
        return ""

    class Meta:
        model = Component
        fields = "__all__"


class ComponentNameSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "component_name_version"]
