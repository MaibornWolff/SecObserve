from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from application.rules.api.serializers import (
    GeneralRuleSerializer,
    ProductRuleSerializer,
)
from application.rules.api.filters import GeneralRuleFilter, ProductRuleFilter
from application.rules.api.permissions import (
    UserHasGeneralRulePermission,
    UserHasProductRulePermission,
)
from application.rules.queries.rule import get_general_rules, get_product_rules
from application.rules.models import Rule


class GeneralRuleViewSet(ModelViewSet):
    serializer_class = GeneralRuleSerializer
    filterset_class = GeneralRuleFilter
    queryset = Rule.objects.none()
    permission_classes = (IsAuthenticated, UserHasGeneralRulePermission)

    def get_queryset(self):
        return get_general_rules()


class ProductRuleViewSet(ModelViewSet):
    serializer_class = ProductRuleSerializer
    filterset_class = ProductRuleFilter
    queryset = Rule.objects.none()
    permission_classes = (IsAuthenticated, UserHasProductRulePermission)

    def get_queryset(self):
        return get_product_rules()
