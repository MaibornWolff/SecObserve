import json
from typing import Any

import jsonpickle
from constance import config
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_501_NOT_IMPLEMENTED,
)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from application.vex.api.filters import CSAFFilter, OpenVEXFilter
from application.vex.api.serializers import (
    CSAFDocumentCreateSerializer,
    CSAFDocumentUpdateSerializer,
    CSAFSerializer,
    OpenVEXDocumentCreateSerializer,
    OpenVEXDocumentUpdateSerializer,
    OpenVEXSerializer,
)
from application.vex.models import CSAF, OpenVEX
from application.vex.services.csaf import (
    CSAFCreateParameters,
    CSAFUpdateParameters,
    create_csaf_document,
    update_csaf_document,
)
from application.vex.services.open_vex import (
    create_open_vex_document,
    update_open_vex_document,
)

VEX_TYPE_CSAF = "csaf"
VEX_TYPE_OPENVEX = "openvex"


class CSAFDocumentCreateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=CSAFDocumentCreateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)

        serializer = CSAFDocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        unique_vulnerability_names = []
        if serializer.validated_data.get("vulnerability_names"):
            unique_vulnerability_names = _remove_duplicates_keep_order(
                serializer.validated_data.get("vulnerability_names")
            )

        csaf_create_parameters = CSAFCreateParameters(
            product_id=serializer.validated_data.get("product_id"),
            vulnerability_names=unique_vulnerability_names,
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            title=serializer.validated_data.get("title"),
            publisher_name=serializer.validated_data.get("publisher_name"),
            publisher_category=serializer.validated_data.get("publisher_category"),
            publisher_namespace=serializer.validated_data.get("publisher_namespace"),
            tracking_status=serializer.validated_data.get("tracking_status"),
        )

        csaf_document = create_csaf_document(csaf_create_parameters)

        if not csaf_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(
            content=_object_to_json(csaf_document, VEX_TYPE_CSAF),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=csaf_"
            + csaf_document.get_base_id()
            + "_"
            + f"{int(csaf_document.document.tracking.version):04d}"
            + ".json"
        )
        return response


class CSAFDocumentUpdateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=CSAFDocumentUpdateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    def post(self, request, document_base_id=None):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)

        serializer = CSAFDocumentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        csaf_update_parameters = CSAFUpdateParameters(
            document_base_id=document_base_id,
            publisher_name=serializer.validated_data.get("publisher_name"),
            publisher_category=serializer.validated_data.get("publisher_category"),
            publisher_namespace=serializer.validated_data.get("publisher_namespace"),
            tracking_status=serializer.validated_data.get("tracking_status"),
        )

        csaf_document = update_csaf_document(csaf_update_parameters)

        if not csaf_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(
            content=_object_to_json(csaf_document, VEX_TYPE_CSAF),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=csaf_"
            + csaf_document.get_base_id()
            + "_"
            + f"{int(csaf_document.document.tracking.version):04d}"
            + ".json"
        )
        return response


class CSAFViewSet(
    GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
):
    serializer_class = CSAFSerializer
    queryset = CSAF.objects.all()
    filterset_class = CSAFFilter
    filter_backends = [DjangoFilterBackend]

    def destroy(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().retrieve(request, *args, **kwargs)


class OpenVEXDocumentCreateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentCreateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)

        serializer = OpenVEXDocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        unique_vulnerability_names = []
        if serializer.validated_data.get("vulnerability_names"):
            unique_vulnerability_names = _remove_duplicates_keep_order(
                serializer.validated_data.get("vulnerability_names")
            )

        open_vex_document = create_open_vex_document(
            product_id=serializer.validated_data.get("product_id"),
            vulnerability_names=unique_vulnerability_names,
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            author=serializer.validated_data.get("author"),
            role=serializer.validated_data.get("role"),
        )

        if not open_vex_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(
            content=_object_to_json(open_vex_document, VEX_TYPE_OPENVEX),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=openvex_"
            + open_vex_document.get_base_id()
            + "_"
            + f"{open_vex_document.version:04d}"
            + ".json"
        )
        return response


class OpenVEXDocumentUpdateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentUpdateSerializer,
        responses={HTTP_200_OK: bytes},
    )
    @action(detail=True, methods=["post"])
    def post(self, request, document_base_id=None):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)

        serializer = OpenVEXDocumentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        open_vex_document = update_open_vex_document(
            document_base_id,
            author=serializer.validated_data.get("author"),
            role=serializer.validated_data.get("role"),
        )

        if not open_vex_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(
            content=_object_to_json(open_vex_document, VEX_TYPE_OPENVEX),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=openvex_"
            + open_vex_document.get_base_id()
            + "_"
            + f"{open_vex_document.version:04d}"
            + ".json"
        )
        return response


class OpenVEXViewSet(
    GenericViewSet, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
):
    serializer_class = OpenVEXSerializer
    queryset = OpenVEX.objects.all()
    filterset_class = OpenVEXFilter
    filter_backends = [DjangoFilterBackend]

    def destroy(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not config.FEATURE_VEX:
            return Response(status=HTTP_501_NOT_IMPLEMENTED)
        return super().retrieve(request, *args, **kwargs)


def _object_to_json(object_to_encode: Any, vex_type: str) -> str:
    json_string = jsonpickle.encode(object_to_encode, unpicklable=False)
    json_dict = json.loads(json_string)
    json_dict = _remove_empty_elements(json_dict)
    if vex_type == VEX_TYPE_OPENVEX:
        json_dict = _change_keys(json_dict)
    return json.dumps(json_dict, indent=4)


def _remove_empty_elements(d: dict) -> dict:
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (_remove_empty_elements(v) for v in d) if not empty(v)]

    return {
        k: v
        for k, v in ((k, _remove_empty_elements(v)) for k, v in d.items())
        if not empty(v)
    }


# Change all keys with the value 'id' to '@id' and
# all keys with the value 'context' to '@context' in a dictionary recursively
def _change_keys(d: dict) -> dict:
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [_change_keys(v) for v in d]

    return {
        k.replace("id", "@id").replace("context", "@context"): _change_keys(v)
        for k, v in d.items()
    }


# remove duplicates from a list and keep the order
def _remove_duplicates_keep_order(items: list) -> list:
    seen: set[Any] = set()
    seen_add = seen.add
    return [x for x in items if not (x in seen or seen_add(x))]
