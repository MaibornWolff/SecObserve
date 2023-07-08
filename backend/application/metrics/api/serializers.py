from rest_framework.serializers import ModelSerializer, SerializerMethodField

from application.metrics.models import Product_Metrics


class ProductMetricsSerializer(ModelSerializer):
    product_name = SerializerMethodField()

    class Meta:
        model = Product_Metrics
        fields = "__all__"

    def get_product_name(self, obj: Product_Metrics):
        return obj.product.name
