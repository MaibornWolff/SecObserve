from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.queries.parser import get_parser_by_id, get_parser_by_name
from application.core.queries.product import get_product_by_id, get_product_by_name
from application.import_observations.api.filters import ApiConfigurationFilter
from application.import_observations.api.permissions import (
    UserHasApiConfigurationPermission,
)
from application.import_observations.api.serializers import (
    ApiConfigurationSerializer,
    ApiImportObservationsByIdRequestSerializer,
    ApiImportObservationsByNameRequestSerializer,
    FileUploadObservationsByIdRequestSerializer,
    FileUploadObservationsByNameRequestSerializer,
    ImportObservationsResponseSerializer,
)
from application.import_observations.models import Api_Configuration
from application.import_observations.queries.api_configuration import (
    get_api_configuration_by_id,
    get_api_configuration_by_name,
    get_api_configurations,
)
from application.import_observations.services.import_observations import (
    api_import_observations,
    file_upload_observations,
)


class ApiImportObservationsById(APIView):
    @extend_schema(
        request=ApiImportObservationsByIdRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request, format=None):
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

        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")

        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = api_import_observations(
            api_configuration, service, docker_image_name_tag, endpoint_url
        )

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
    def post(self, request, format=None):
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

        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = api_import_observations(
            api_configuration, service, docker_image_name_tag, endpoint_url
        )

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
    def post(self, request, format=None):
        request_serializer = FileUploadObservationsByIdRequestSerializer(
            data=request.data
        )
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        product_id = request_serializer.validated_data.get("product")
        product = get_product_by_id(product_id)
        if not product:
            raise ValidationError(f"Product {product} does not exist")

        user_has_permission_or_403(product, Permissions.Product_Import_Observations)

        parser_id = request_serializer.validated_data.get("parser")
        parser = get_parser_by_id(parser_id)
        if not parser:
            raise ValidationError(f"Parser {parser} does not exist")

        file = request_serializer.validated_data.get("file")
        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")

        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = file_upload_observations(
            product, parser, file, service, docker_image_name_tag, endpoint_url
        )

        response_data = {
            "observations_new": observations_new,
            "observations_updated": observations_updated,
            "observations_resolved": observations_resolved,
        }
        return Response(response_data)


class FileUploadObservationsByName(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=FileUploadObservationsByNameRequestSerializer,
        responses={status.HTTP_200_OK: ImportObservationsResponseSerializer},
    )
    def post(self, request, format=None):
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

        parser_name = request_serializer.validated_data.get("parser_name")
        parser = get_parser_by_name(parser_name)
        if not parser:
            raise ValidationError(f"Parser {parser_name} does not exist")

        file = request_serializer.validated_data.get("file")
        service = request_serializer.validated_data.get("service")
        docker_image_name_tag = request_serializer.validated_data.get(
            "docker_image_name_tag"
        )
        endpoint_url = request_serializer.validated_data.get("endpoint_url")

        (
            observations_new,
            observations_updated,
            observations_resolved,
        ) = file_upload_observations(
            product, parser, file, service, docker_image_name_tag, endpoint_url
        )

        response_data = {
            "observations_new": observations_new,
            "observations_updated": observations_updated,
            "observations_resolved": observations_resolved,
        }
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
