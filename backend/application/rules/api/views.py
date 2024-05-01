from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.rules.api.filters import GeneralRuleFilter, ProductRuleFilter
from application.rules.api.permissions import (
    UserHasGeneralRulePermission,
    UserHasProductRulePermission,
)
from application.rules.api.serializers import (
    GeneralRuleSerializer,
    ProductRuleSerializer,
    RuleApprovalSerializer,
)
from application.rules.models import Rule
from application.rules.queries.rule import (
    get_general_rule_by_id,
    get_general_rules,
    get_product_rule_by_id,
    get_product_rules,
)
from application.rules.services.approval import rule_approval


class GeneralRuleViewSet(ModelViewSet):
    serializer_class = GeneralRuleSerializer
    filterset_class = GeneralRuleFilter
    queryset = Rule.objects.none()
    permission_classes = (IsAuthenticated, UserHasGeneralRulePermission)

    def get_queryset(self):
        return get_general_rules()

    @extend_schema(
        methods=["PATCH"],
        request=RuleApprovalSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["patch"])
    def approval(self, request, pk=None):
        request_serializer = RuleApprovalSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        general_rule = get_general_rule_by_id(pk)
        if not general_rule:
            raise NotFound(f"General rule {pk} not found")

        rule_approval(
            general_rule,
            request_serializer.validated_data.get("approval_status"),
            request_serializer.validated_data.get("approval_remark"),
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRuleViewSet(ModelViewSet):
    serializer_class = ProductRuleSerializer
    filterset_class = ProductRuleFilter
    queryset = Rule.objects.none()
    permission_classes = (IsAuthenticated, UserHasProductRulePermission)

    def get_queryset(self):
        return get_product_rules()

    @extend_schema(
        methods=["PATCH"],
        request=RuleApprovalSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["patch"])
    def approval(self, request, pk=None):
        request_serializer = RuleApprovalSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product_rule = get_product_rule_by_id(pk)
        if not product_rule:
            raise NotFound(f"Product rule {pk} not found")

        user_has_permission_or_403(product_rule, Permissions.Product_Rule_Approval)

        rule_approval(
            product_rule,
            request_serializer.validated_data.get("approval_status"),
            request_serializer.validated_data.get("approval_remark"),
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
