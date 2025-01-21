from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Branch
from application.core.queries.branch import get_branch_by_id, get_branch_by_name
from application.core.queries.product import get_product_by_id, get_product_by_name
from application.import_observations.api.filters import (
    ApiConfigurationFilter,
    ParserFilter,
    VulnerabilityCheckFilter,
)
from application.import_observations.api.permissions import (
    UserHasApiConfigurationPermission,
    UserHasVulnerabilityCheckPermission,
)
from application.import_observations.api.serializers import (
    ApiConfigurationSerializer,
    ApiImportObservationsByIdRequestSerializer,
    ApiImportObservationsByNameRequestSerializer,
    FileUploadObservationsByIdRequestSerializer,
    FileUploadObservationsByNameRequestSerializer,
    ImportObservationsResponseSerializer,
    ParserSerializer,
    VulnerabilityCheckSerializer,
)
from application.import_observations.models import (
    Api_Configuration,
    Parser,
    Vulnerability_Check,
)
from application.import_observations.queries.api_configuration import (
    get_api_configuration_by_id,
    get_api_configuration_by_name,
    get_api_configurations,
)
from application.import_observations.queries.vulnerability_check import (
    get_vulnerability_checks,
)
from application.import_observations.services.import_observations import (
    ApiImportParameters,
    FileUploadParameters,
    api_import_observations,
    file_upload_observations,
)
from application.import_observations.services.osv_scanner import scan_product


class ApiImportObservationsById(APIView):
    @extend_schema(
        request=ApiImportObservationsByIdRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request):
        request_serializer = ApiImportObservationsByIdRequestSerializer(
            data=request.data
        )
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        api_configuration_id = request_serializer.validated_data.get(
            "api_configuration"
        )
        api_configuration = get_api_configuration_by_id(api_configuration_id)
        if not api_configuration:
            raise ValidationError(
                f"API Configuration {api_configuration} does not exist"
            )

        user_has_permission_or_403(
            api_configuration.product, Permissions.Product_Import_Observations
        )

        branch = None
        branch_id = request_serializer.validated_data.get("branch")
        if branch_id:
            branch = get_branch_by_id(api_configuration.product, branch_id)
            if not branch:
                raise ValidationError(
                    f"Branch {branch_id} does not exist for product {api_configuration.product}"
                )

        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")
        kubernetes_cluster = request_serializer.validated_data.get("kubernetes_cluster")

        api_import_parameters = ApiImportParameters(
            api_configuration=api_configuration,
            branch=branch,
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
        )

        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = api_import_observations(api_import_parameters)

        response_data = {
            "observations_new": observations_new,
            "observations_updated": observations_updated,
            "observations_resolved": observations_resolved,
        }
        return Response(response_data)


class ApiImportObservationsByName(APIView):
    @extend_schema(
        request=ApiImportObservationsByNameRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request):
        request_serializer = ApiImportObservationsByNameRequestSerializer(
            data=request.data
        )
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product_name = request_serializer.validated_data.get("product_name")
        product = get_product_by_name(product_name)
        if not product:
            raise ValidationError(f"Product {product_name} does not exist")

        user_has_permission_or_403(product, Permissions.Product_Import_Observations)

        branch = None
        branch_name = request_serializer.validated_data.get("branch_name")
        if branch_name:
            branch = get_branch_by_name(product, branch_name)
            if not branch:
                branch = Branch.objects.create(product=product, name=branch_name)

        api_configuration_name = request_serializer.validated_data.get(
            "api_configuration_name"
        )
        api_configuration = get_api_configuration_by_name(
            product, api_configuration_name
        )
        if not api_configuration:
            raise ValidationError(
                f"API Configuration {api_configuration_name} does not exist for product {product.name}"
            )

        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")
        kubernetes_cluster = request_serializer.validated_data.get("kubernetes_cluster")

        api_import_parameters = ApiImportParameters(
            api_configuration=api_configuration,
            branch=branch,
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
        )
        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = api_import_observations(api_import_parameters)

        response_data = {
            "observations_new": observations_new,
            "observations_updated": observations_updated,
            "observations_resolved": observations_resolved,
        }
        return Response(response_data)


class FileUploadObservationsById(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=FileUploadObservationsByIdRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request):  # pylint: disable=too-many-locals
        # not too much we can do about this
        request_serializer = FileUploadObservationsByIdRequestSerializer(
            data=request.data
        )
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product_id = request_serializer.validated_data.get("product")
        product = get_product_by_id(product_id)
        if not product:
            raise ValidationError(f"Product {product_id} does not exist")

        user_has_permission_or_403(product, Permissions.Product_Import_Observations)

        branch = None
        branch_id = request_serializer.validated_data.get("branch")
        if branch_id:
            branch = get_branch_by_id(product, branch_id)
            if not branch:
                raise ValidationError(
                    f"Branch {branch_id} does not exist for product {product}"
                )

        file = request_serializer.validated_data.get("file")
        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")
        kubernetes_cluster = request_serializer.validated_data.get("kubernetes_cluster")
        suppress_licenses = request_serializer.validated_data.get(
            "suppress_licenses", False
        )

        file_upload_parameters = FileUploadParameters(
            product=product,
            branch=branch,
            file=file,
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            observations_new,
            observations_updated,
            observations_resolved,
            license_components_new,
            license_components_updated,
            license_components_deleted,
        ) = file_upload_observations(file_upload_parameters)

        num_observations = (
            observations_new + observations_updated + observations_resolved
        )
        num_license_components = (
            license_components_new
            + license_components_updated
            + license_components_deleted
        )

        response_data = {}
        if num_observations > 0 or num_license_components == 0:
            response_data["observations_new"] = observations_new
            response_data["observations_updated"] = observations_updated
            response_data["observations_resolved"] = observations_resolved
        if num_license_components > 0:
            response_data["license_components_new"] = license_components_new
            response_data["license_components_updated"] = license_components_updated
            response_data["license_components_deleted"] = license_components_deleted

        return Response(response_data)


class FileUploadObservationsByName(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=FileUploadObservationsByNameRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request):  # pylint: disable=too-many-locals
        # not too much we can do about this
        request_serializer = FileUploadObservationsByNameRequestSerializer(
            data=request.data
        )
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product_name = request_serializer.validated_data.get("product_name")
        product = get_product_by_name(product_name)
        if not product:
            raise ValidationError(f"Product {product_name} does not exist")

        user_has_permission_or_403(product, Permissions.Product_Import_Observations)

        branch = None
        branch_name = request_serializer.validated_data.get("branch_name")
        if branch_name:
            branch = get_branch_by_name(product, branch_name)
            if not branch:
                branch = Branch.objects.create(product=product, name=branch_name)

        file = request_serializer.validated_data.get("file")
        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")
        kubernetes_cluster = request_serializer.validated_data.get("kubernetes_cluster")
        suppress_licenses = request_serializer.validated_data.get(
            "suppress_licenses", False
        )

        file_upload_parameters = FileUploadParameters(
            product=product,
            branch=branch,
            file=file,
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            observations_new,
            observations_updated,
            observations_resolved,
            license_components_new,
            license_components_updated,
            license_components_deleted,
        ) = file_upload_observations(file_upload_parameters)

        num_observations = (
            observations_new + observations_updated + observations_resolved
        )
        num_license_components = (
            license_components_new
            + license_components_updated
            + license_components_deleted
        )

        response_data = {}
        if num_observations > 0 or num_license_components == 0:
            response_data["observations_new"] = observations_new
            response_data["observations_updated"] = observations_updated
            response_data["observations_resolved"] = observations_resolved
        if num_license_components > 0:
            response_data["license_components_new"] = license_components_new
            response_data["license_components_updated"] = license_components_updated
            response_data["license_components_deleted"] = license_components_deleted

        return Response(response_data)


class ApiConfigurationViewSet(ModelViewSet):
    serializer_class = ApiConfigurationSerializer
    filterset_class = ApiConfigurationFilter
    permission_classes = (IsAuthenticated, UserHasApiConfigurationPermission)
    queryset = Api_Configuration.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]

    def get_queryset(self):
        return get_api_configurations()


class VulnerabilityCheckViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = VulnerabilityCheckSerializer
    filterset_class = VulnerabilityCheckFilter
    permission_classes = (IsAuthenticated, UserHasVulnerabilityCheckPermission)
    queryset = Vulnerability_Check.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_vulnerability_checks()


class ParserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = ParserSerializer
    filterset_class = ParserFilter
    queryset = Parser.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]


class ScanOSVProductView(APIView):
    @action(detail=True, methods=["post"])
    def post(self, request, product_id: int):
        product = get_product_by_id(product_id)
        if not product:
            return Response(status=HTTP_404_NOT_FOUND)

        user_has_permission_or_403(product, Permissions.Product_Scan_OSV)

        scan_product(product)
        return Response(status=HTTP_204_NO_CONTENT)
