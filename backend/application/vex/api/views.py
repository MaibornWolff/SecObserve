import json
import re
from typing import Any, Optional, Union
from urllib.parse import urlparse

import jsonpickle
from django.db.models import QuerySet
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.commons.api.permissions import UserHasSuperuserPermission
from application.vex.api.filters import (
    CSAFBranchFilter,
    CSAFFilter,
    CSAFVulnerabilityFilter,
    OpenVEXBranchFilter,
    OpenVEXFilter,
    OpenVEXVulnerabilityFilter,
    VEXCounterFilter,
    VEXDocumentFilter,
    VEXStatementFilter,
)
from application.vex.api.permissions import (
    UserHasVEXCounterPermission,
    UserHasVEXPermission,
)
from application.vex.api.serializers import (
    CSAFBranchSerializer,
    CSAFDocumentCreateSerializer,
    CSAFDocumentUpdateSerializer,
    CSAFSerializer,
    CSAFVulnerabilitySerializer,
    OpenVEXBranchSerializer,
    OpenVEXDocumentCreateSerializer,
    OpenVEXDocumentUpdateSerializer,
    OpenVEXSerializer,
    OpenVEXVulnerabilitySerializer,
    VEXCounterSerializer,
    VEXDocumentSerializer,
    VEXImportSerializer,
    VEXStatementSerializer,
)
from application.vex.models import (
    CSAF,
    CSAF_Branch,
    CSAF_Vulnerability,
    OpenVEX,
    OpenVEX_Branch,
    OpenVEX_Vulnerability,
    VEX_Counter,
    VEX_Document,
    VEX_Statement,
)
from application.vex.queries.csaf import (
    get_csaf_branches,
    get_csaf_vulnerabilities,
    get_csafs,
)
from application.vex.queries.openvex import (
    get_openvex_branches,
    get_openvex_s,
    get_openvex_vulnerabilities,
)
from application.vex.queries.vex_document import get_vex_documents, get_vex_statements
from application.vex.services.csaf_generator import (
    CSAFCreateParameters,
    CSAFUpdateParameters,
    create_csaf_document,
    update_csaf_document,
)
from application.vex.services.openvex_generator import (
    OpenVEXCreateParameters,
    OpenVEXUpdateParameters,
    create_openvex_document,
    update_openvex_document,
)
from application.vex.services.vex_import import import_vex

VEX_TYPE_CSAF = "csaf"
VEX_TYPE_OPENVEX = "openvex"


class CSAFDocumentCreateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=CSAFDocumentCreateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request: Request) -> HttpResponse:
        serializer = CSAFDocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        unique_vulnerability_names = []
        if serializer.validated_data.get("vulnerability_names"):
            unique_vulnerability_names = _remove_duplicates_keep_order(
                serializer.validated_data.get("vulnerability_names")
            )

        unique_branch_names = (
            _remove_duplicates_keep_order(serializer.validated_data.get("branch_names"))
            if serializer.validated_data.get("branch_names")
            else []
        )

        csaf_create_parameters = CSAFCreateParameters(
            product_id=serializer.validated_data.get("product"),
            vulnerability_names=unique_vulnerability_names,
            branch_names=unique_branch_names,
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            title=serializer.validated_data.get("title"),
            publisher_name=serializer.validated_data.get("publisher_name"),
            publisher_category=serializer.validated_data.get("publisher_category"),
            publisher_namespace=serializer.validated_data.get("publisher_namespace"),
            tracking_status=serializer.validated_data.get("tracking_status"),
            tlp_label=serializer.validated_data.get("tlp_label"),
        )

        csaf_document = create_csaf_document(csaf_create_parameters)

        if not csaf_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(  # pylint: disable=http-response-with-content-type-json
            # HTTPResponse gives more control about JSON serialization
            content=_object_to_json(csaf_document, VEX_TYPE_CSAF),
            content_type="application/json",
        )
        response["Content-Disposition"] = (
            f"attachment; filename={_get_csaf_filename(csaf_document.document.tracking.id)}.json"
        )
        return response


class CSAFDocumentUpdateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=CSAFDocumentUpdateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    def post(self, request: Request, document_id_prefix: str, document_base_id: str) -> HttpResponse:
        serializer = CSAFDocumentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        csaf_update_parameters = CSAFUpdateParameters(
            document_id_prefix=document_id_prefix,
            document_base_id=document_base_id,
            publisher_name=serializer.validated_data.get("publisher_name"),
            publisher_category=serializer.validated_data.get("publisher_category"),
            publisher_namespace=serializer.validated_data.get("publisher_namespace"),
            tracking_status=serializer.validated_data.get("tracking_status"),
            tlp_label=serializer.validated_data.get("tlp_label"),
        )

        csaf_document = update_csaf_document(csaf_update_parameters)

        if not csaf_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(  # pylint: disable=http-response-with-content-type-json
            # HTTPResponse gives more control about JSON serialization
            content=_object_to_json(csaf_document, VEX_TYPE_CSAF),
            content_type="application/json",
        )
        response["Content-Disposition"] = (
            f"attachment; filename={_get_csaf_filename(csaf_document.document.tracking.id)}.json"
        )
        return response


class CSAFViewSet(GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = CSAFSerializer
    queryset = CSAF.objects.none()
    filterset_class = CSAFFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, UserHasVEXPermission)

    def get_queryset(self) -> QuerySet[CSAF]:
        return get_csafs()


class CSAFVulnerabilityViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = CSAFVulnerabilitySerializer
    queryset = CSAF_Vulnerability.objects.none()
    filterset_class = CSAFVulnerabilityFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[CSAF_Vulnerability]:
        return get_csaf_vulnerabilities()


class CSAFBranchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = CSAFBranchSerializer
    queryset = CSAF_Branch.objects.none()
    filterset_class = CSAFBranchFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[CSAF_Branch]:
        return get_csaf_branches()


class OpenVEXDocumentCreateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentCreateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request: Request) -> HttpResponse:
        serializer = OpenVEXDocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        unique_vulnerability_names = (
            _remove_duplicates_keep_order(serializer.validated_data.get("vulnerability_names"))
            if serializer.validated_data.get("vulnerability_names")
            else []
        )

        unique_branch_names = (
            _remove_duplicates_keep_order(serializer.validated_data.get("branch_names"))
            if serializer.validated_data.get("branch_names")
            else []
        )

        parameters = OpenVEXCreateParameters(
            product_id=serializer.validated_data.get("product"),
            vulnerability_names=unique_vulnerability_names,
            branch_names=unique_branch_names,
            id_namespace=serializer.validated_data.get("id_namespace"),
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            author=serializer.validated_data.get("author"),
            role=serializer.validated_data.get("role"),
        )

        openvex_document = create_openvex_document(parameters)

        if not openvex_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(  # pylint: disable=http-response-with-content-type-json
            # HTTPResponse gives more control about JSON serialization
            content=_object_to_json(openvex_document, VEX_TYPE_OPENVEX),
            content_type="application/json",
        )
        response["Content-Disposition"] = "attachment; filename=" + _get_openvex_filename(
            openvex_document.id, openvex_document.version
        )
        return response


class OpenVEXDocumentUpdateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentUpdateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request: Request, document_id_prefix: str, document_base_id: str) -> HttpResponse:
        serializer = OpenVEXDocumentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        parameters = OpenVEXUpdateParameters(
            document_id_prefix=document_id_prefix,
            document_base_id=document_base_id,
            author=serializer.validated_data.get("author"),
            role=serializer.validated_data.get("role"),
        )

        openvex_document = update_openvex_document(parameters)

        if not openvex_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(  # pylint: disable=http-response-with-content-type-json
            # HTTPResponse gives more control about JSON serialization
            content=_object_to_json(openvex_document, VEX_TYPE_OPENVEX),
            content_type="application/json",
        )
        response["Content-Disposition"] = "attachment; filename=" + _get_openvex_filename(
            openvex_document.id, openvex_document.version
        )
        return response


class OpenVEXViewSet(GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = OpenVEXSerializer
    queryset = OpenVEX.objects.none()
    filterset_class = OpenVEXFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, UserHasVEXPermission)

    def get_queryset(self) -> QuerySet[OpenVEX]:
        return get_openvex_s()


class OpenVEXVulnerabilityViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = OpenVEXVulnerabilitySerializer
    queryset = OpenVEX_Vulnerability.objects.none()
    filterset_class = OpenVEXVulnerabilityFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[OpenVEX_Vulnerability]:
        return get_openvex_vulnerabilities()


class OpenVEXBranchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = OpenVEXBranchSerializer
    queryset = OpenVEX_Branch.objects.none()
    filterset_class = OpenVEXBranchFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self) -> QuerySet[OpenVEX_Branch]:
        return get_openvex_branches()


class VEXCounterViewSet(ModelViewSet):
    serializer_class = VEXCounterSerializer
    queryset = VEX_Counter.objects.all()
    filterset_class = VEXCounterFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, UserHasVEXCounterPermission)


class VEXDocumentViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = VEXDocumentSerializer
    queryset = VEX_Document.objects.none()
    filterset_class = VEXDocumentFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, UserHasSuperuserPermission)

    def get_queryset(self) -> QuerySet[VEX_Document]:
        return get_vex_documents()


class VEXStatementViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = VEXStatementSerializer
    queryset = VEX_Statement.objects.none()
    filterset_class = VEXStatementFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated, UserHasSuperuserPermission)

    def get_queryset(self) -> QuerySet[VEX_Statement]:
        return get_vex_statements()


class VEXImportView(APIView):
    permission_classes = (IsAuthenticated, UserHasSuperuserPermission)
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=VEXImportSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    def post(self, request: Request) -> Response:
        request_serializer = VEXImportSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        import_vex(request_serializer.validated_data.get("file"))

        return Response(status=HTTP_204_NO_CONTENT)


def _object_to_json(object_to_encode: Any, vex_type: str) -> str:
    jsonpickle.set_encoder_options("json", ensure_ascii=False)
    json_string = jsonpickle.encode(object_to_encode, unpicklable=False)

    json_dict = json.loads(json_string)
    json_dict = _remove_empty_elements(json_dict)
    if vex_type == VEX_TYPE_OPENVEX:
        json_dict = _change_keys_context(json_dict)
        json_dict = _change_keys_id(json_dict)

    return json.dumps(json_dict, indent=4, sort_keys=True, ensure_ascii=False)


def _remove_empty_elements(d: dict) -> dict:
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x: Optional[Union[dict | list]]) -> bool:
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (_remove_empty_elements(v) for v in d) if not empty(v)]

    return {k: v for k, v in ((k, _remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


# Change all keys with the value 'id' to '@id' and
# all keys with the value 'context' to '@context' in a dictionary recursively
def _change_keys_context(d: dict) -> dict:
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [_change_keys_context(v) for v in d]

    return {k.replace("context", "@context"): _change_keys_context(v) for k, v in d.items()}


# Change all keys with the value 'id' to '@id' and
# all keys with the value 'context' to '@context' in a dictionary recursively
def _change_keys_id(d: dict) -> dict:
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [_change_keys_id(v) for v in d]

    return {re.sub("^id$", "@id", k): _change_keys_id(v) for k, v in d.items()}


# remove duplicates from a list and keep the order
def _remove_duplicates_keep_order(items: list) -> list:
    seen: set[Any] = set()
    seen_add = seen.add
    return [x for x in items if not (x in seen or seen_add(x))]


def _get_csaf_filename(document_id: str) -> str:
    filename = document_id.lower()
    # find characters with regex [^+\-a-z0-9]+ and replace them with _
    filename = re.sub(r"[^+\-a-z0-9]+", "_", filename)
    # remove multiple underscores
    filename = re.sub(r"__+", "_", filename)
    return filename


def _get_openvex_filename(document_id: str, version: int) -> str:
    parse_result = urlparse(document_id)
    path = parse_result.path
    # get last part of the path
    path = path.split("/")[-1]

    return f"{path}_{version:04d}.json"
