from rest_framework.serializers import ModelSerializer, ValidationError

from application.core.api.serializers_product import NestedProductSerializer
from application.rules.models import Rule


class GeneralRuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        exclude = ["product"]

    def validate(self, attrs):
        if not attrs.get("parser") and not attrs.get("scanner_prefix"):
            raise ValidationError("Either Parser or Scanner Prefix must be set")

        return super().validate(attrs)


class ProductRuleSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product", read_only=True)

    class Meta:
        model = Rule
        fields = "__all__"

    def validate_product(self, value):
        self.instance: Rule
        if self.instance and self.instance.product != value:
            raise ValidationError("Product cannot be changed")

        return value

    def validate(self, attrs):
        if not attrs.get("parser") and not attrs.get("scanner_prefix"):
            raise ValidationError("Either Parser or Scanner Prefix must be set")

        return super().validate(attrs)
