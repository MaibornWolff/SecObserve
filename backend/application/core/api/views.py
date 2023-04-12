import csv
from tempfile import NamedTemporaryFile

from django.db.models import Prefetch
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.api.filters import (
    ObservationFilter,
    ParserFilter,
    ProductFilter,
    ProductMemberFilter,
)
from application.core.api.permissions import (
    UserHasObservationPermission,
    UserHasProductMemberPermission,
    UserHasProductPermission,
)
from application.core.api.serializers import (
    EvidenceSerializer,
    ObservationAssessmentSerializer,
    ObservationCreateSerializer,
    ObservationListSerializer,
    ObservationRemoveAssessmentSerializer,
    ObservationSerializer,
    ObservationUpdateSerializer,
    ParserSerializer,
    ProductMemberSerializer,
    ProductSerializer,
)
from application.core.models import (
    Observation,
    Observation_Log,
    Parser,
    Product,
    Product_Member,
)
from application.core.queries.observation import (
    get_evidences,
    get_observation_by_id,
    get_observations,
)
from application.core.queries.product import (
    get_product_by_id,
    get_product_members,
    get_products,
)
from application.core.services.assessment import remove_assessment, save_assessment
from application.core.services.export_observations import (
    export_observations_csv,
    export_observations_excel,
)
from application.metrics.services.metrics import get_codecharta_metrics
from application.rules.services.rule_engine import Rule_Engine


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = (IsAuthenticated, UserHasProductPermission)
    queryset = Product.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_products()

    @extend_schema(
        methods=["GET"],
        responses={200: None},
    )
    @action(detail=True, methods=["get"])
    def export_codecharta_metrics(self, request, pk=None):
        product = self.__get_product(pk)

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="secobserve_codecharta_metrics.csv"'

        writer = csv.DictWriter(
            response,
            fieldnames=[
                "source_file",
                "Vulnerabilities_Total".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_CRITICAL}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_HIGH}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_LOW}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_NONE}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_UNKOWN}".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_HIGH}_and_above".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_MEDIUM}_and_above".lower(),
                f"Vulnerabilities_{Observation.SEVERITY_LOW}_and_above".lower(),
            ],
        )
        writer.writeheader()
        for row in get_codecharta_metrics(product):
            writer.writerow(row)

        return response

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
        if status and (status, status) not in Observation.STATUS_CHOICES:
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
        if status and (status, status) not in Observation.STATUS_CHOICES:
            raise ValidationError(f"Status {status} is not a valid choice")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=observations.csv"

        export_observations_csv(response, product, status)

        return response

    @extend_schema(
        methods=["PUT"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["put"])
    def apply_rules(self, request, pk=None):
        product = self.__get_product(pk)
        user_has_permission_or_403(product, Permissions.Product_Rule_Apply)

        for parser in Parser.objects.all():
            rule_engine = Rule_Engine(product, parser)
            rule_engine.apply_all_rules_for_product_and_parser()

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
            .select_related("parser")
            .prefetch_related(
                Prefetch(
                    "observation_logs",
                    queryset=Observation_Log.objects.order_by("-created"),
                )
            )
        )

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

        return Response()


class EvidenceViewSet(GenericViewSet, RetrieveModelMixin):
    serializer_class = EvidenceSerializer
    queryset = Observation.objects.none()

    def get_queryset(self):
        return get_evidences()
