from tempfile import NamedTemporaryFile
from typing import Any

from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.commons.services.global_request import get_current_user
from application.core.api.filters import (
    BranchFilter,
    EvidenceFilter,
    ObservationFilter,
    ParserFilter,
    PotentialDuplicateFilter,
    ProductFilter,
    ProductGroupFilter,
    ProductMemberFilter,
    ServiceFilter,
)
from application.core.api.permissions import (
    UserHasBranchPermission,
    UserHasObservationPermission,
    UserHasProductMemberPermission,
    UserHasProductPermission,
    UserHasServicePermission,
)
from application.core.api.serializers import (
    BranchSerializer,
    EvidenceSerializer,
    ObservationAssessmentSerializer,
    ObservationBulkAssessmentSerializer,
    ObservationBulkDeleteSerializer,
    ObservationBulkMarkDuplicatesSerializer,
    ObservationCreateSerializer,
    ObservationListSerializer,
    ObservationRemoveAssessmentSerializer,
    ObservationSerializer,
    ObservationUpdateSerializer,
    ParserSerializer,
    PotentialDuplicateSerializer,
    ProductGroupSerializer,
    ProductMemberSerializer,
    ProductSerializer,
    ServiceSerializer,
)
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Parser,
    Potential_Duplicate,
    Product,
    Product_Member,
    Service,
)
from application.core.queries.branch import get_branches
from application.core.queries.observation import (
    get_evidences,
    get_observation_by_id,
    get_observations,
    get_potential_duplicates,
)
from application.core.queries.product import get_product_by_id, get_products
from application.core.queries.product_member import get_product_members
from application.core.queries.service import get_services
from application.core.services.assessment import remove_assessment, save_assessment
from application.core.services.export_observations import (
    export_observations_csv,
    export_observations_excel,
)
from application.core.services.observations_bulk_actions import (
    observations_bulk_assessment,
    observations_bulk_delete,
    observations_bulk_mark_duplicates,
)
from application.core.services.potential_duplicates import (
    set_potential_duplicate_both_ways,
)
from application.core.services.security_gate import check_security_gate
from application.core.types import Status
from application.issue_tracker.services.issue_tracker import (
    push_deleted_observation_to_issue_tracker,
    push_observations_to_issue_tracker,
)
from application.rules.services.rule_engine import Rule_Engine


class ProductGroupViewSet(ModelViewSet):
    serializer_class = ProductGroupSerializer
    filterset_class = ProductGroupFilter
    permission_classes = (IsAuthenticated, UserHasProductPermission)
    queryset = Product.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_products(is_product_group=True)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = (IsAuthenticated, UserHasProductPermission)
    queryset = Product.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return (
            get_products(is_product_group=False)
            .select_related("product_group")
            .select_related("repository_default_branch")
        )

    @extend_schema(
        methods=["GET"],
        responses={200: None},
        parameters=[
            OpenApiParameter(name="status", description="status", type=str),
        ],
    )
    @action(detail=True, methods=["get"])
    def export_observations_excel(self, request, pk=None):
        product = self.__get_product(pk)

        status = self.request.query_params.get("status")
        if status and (status, status) not in Status.STATUS_CHOICES:
            raise ValidationError(f"Status {status} is not a valid choice")

        workbook = export_observations_excel(product, status)

        with NamedTemporaryFile() as tmp:
            workbook.save(
                tmp.name  # nosemgrep: python.lang.correctness.tempfile.flush.tempfile-without-flush
            )
            # export works fine without .flush()
            tmp.seek(0)
            stream = tmp.read()

        response = HttpResponse(
            content=stream,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=observations.xlsx"

        return response

    @extend_schema(
        methods=["GET"],
        responses={200: None},
        parameters=[
            OpenApiParameter(name="status", description="status", type=str),
        ],
    )
    @action(detail=True, methods=["get"])
    def export_observations_csv(self, request, pk=None):
        product = self.__get_product(pk)

        status = self.request.query_params.get("status")
        if status and (status, status) not in Status.STATUS_CHOICES:
            raise ValidationError(f"Status {status} is not a valid choice")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=observations.csv"

        export_observations_csv(response, product, status)

        return response

    @extend_schema(
        methods=["POST"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def apply_rules(self, request, pk=None):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Product_Rule_Apply)

        rule_engine = Rule_Engine(product)
        rule_engine.apply_all_rules_for_product()

        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=ObservationBulkAssessmentSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def observations_bulk_assessment(self, request, pk=None):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Observation_Assessment)

        request_serializer = ObservationBulkAssessmentSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        observations_bulk_assessment(
            product,
            request_serializer.validated_data.get("severity"),
            request_serializer.validated_data.get("status"),
            request_serializer.validated_data.get("comment"),
            request_serializer.validated_data.get("observations"),
        )
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=ObservationBulkMarkDuplicatesSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def observations_bulk_mark_duplicates(self, request, pk=None):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Observation_Assessment)

        request_serializer = ObservationBulkMarkDuplicatesSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        observations_bulk_mark_duplicates(
            product,
            request_serializer.validated_data.get("observation_id"),
            request_serializer.validated_data.get("potential_duplicates"),
        )
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=ObservationBulkDeleteSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def observations_bulk_delete(self, request, pk):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Observation_Delete)

        request_serializer = ObservationBulkDeleteSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        observations_bulk_delete(
            product, request_serializer.validated_data.get("observations")
        )
        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def synchronize_issues(self, request, pk):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Product_Edit)

        observations = Observation.objects.filter(product=product)
        push_observations_to_issue_tracker(product, set(observations))

        return Response(status=HTTP_204_NO_CONTENT)

    def __get_product(self, pk) -> Product:
        if not pk:
            raise ValidationError("No id provided")

        product = get_product_by_id(pk)
        if not product:
            raise NotFound()

        user_has_permission_or_403(product, Permissions.Product_View)

        return product


class ProductMemberViewSet(ModelViewSet):
    serializer_class = ProductMemberSerializer
    filterset_class = ProductMemberFilter
    permission_classes = (IsAuthenticated, UserHasProductMemberPermission)
    queryset = Product_Member.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_product_members().select_related("user")


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    filterset_class = BranchFilter
    permission_classes = (IsAuthenticated, UserHasBranchPermission)
    queryset = Branch.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_branches()

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance: Branch = self.get_object()
        if instance == instance.product.repository_default_branch:
            raise ValidationError("You cannot delete the default branch of a product.")

        return super().destroy(request, *args, **kwargs)


class ServiceViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
):
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilter
    permission_classes = (IsAuthenticated, UserHasServicePermission)
    queryset = Service.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_services()


class ParserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = ParserSerializer
    filterset_class = ParserFilter
    queryset = Parser.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]


class ObservationViewSet(ModelViewSet):
    serializer_class = ObservationSerializer
    filterset_class = ObservationFilter
    permission_classes = (IsAuthenticated, UserHasObservationPermission)
    queryset = Observation.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action == "list":
            return ObservationListSerializer

        if self.action == "create":
            return ObservationCreateSerializer

        if self.action in ["update", "partial_update"]:
            return ObservationUpdateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return (
            get_observations()
            .select_related("product")
            .select_related("product__product_group")
            .select_related("branch")
            .select_related("parser")
        )

    def perform_destroy(self, instance: Observation) -> None:
        product = instance.product
        issue_id = instance.issue_tracker_issue_id
        super().perform_destroy(instance)
        check_security_gate(product)
        push_deleted_observation_to_issue_tracker(product, issue_id, get_current_user())
        product.last_observation_change = timezone.now()
        product.save()

    @extend_schema(
        methods=["PATCH"],
        request=ObservationAssessmentSerializer,
        responses={200: None},
    )
    @action(detail=True, methods=["patch"])
    def assessment(self, request, pk=None):
        request_serializer = ObservationAssessmentSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        observation = get_observation_by_id(pk)
        if not observation:
            raise NotFound(f"Observation {pk} not found")

        user_has_permission_or_403(observation, Permissions.Observation_Assessment)

        new_severity = request_serializer.validated_data.get("severity")
        new_status = request_serializer.validated_data.get("status")
        comment = request_serializer.validated_data.get("comment")

        save_assessment(observation, new_severity, new_status, comment)
        set_potential_duplicate_both_ways(observation)

        return Response()

    @extend_schema(
        methods=["PATCH"],
        request=ObservationRemoveAssessmentSerializer,
        responses={200: None},
    )
    @action(detail=True, methods=["patch"])
    def remove_assessment(self, request, pk=None):
        request_serializer = ObservationRemoveAssessmentSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        observation = get_observation_by_id(pk)
        if not observation:
            raise NotFound(f"Observation {pk} not found")

        user_has_permission_or_403(observation, Permissions.Observation_Assessment)

        comment = request_serializer.validated_data.get("comment")

        remove_assessment(observation, comment)
        set_potential_duplicate_both_ways(observation)

        return Response()


class EvidenceViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = EvidenceSerializer
    filterset_class = EvidenceFilter
    queryset = Evidence.objects.none()

    def get_queryset(self):
        return get_evidences()


class PotentialDuplicateViewSet(GenericViewSet, ListModelMixin):
    serializer_class = PotentialDuplicateSerializer
    filterset_class = PotentialDuplicateFilter
    queryset = Potential_Duplicate.objects.none()

    def get_queryset(self):
        return get_potential_duplicates()
