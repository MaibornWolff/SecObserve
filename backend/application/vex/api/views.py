import json
from typing import Any

import jsonpickle
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

from application.vex.api.filters import OpenVEXFilter
from application.vex.api.serializers import (
    OpenVEXDocumentCreateSerializer,
    OpenVEXDocumentUpdateSerializer,
    OpenVEXSerializer,
)
from application.vex.models import OpenVEX
from application.vex.services.open_vex import (
    create_open_vex_document,
    update_open_vex_document,
)
from constance import config


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

        open_vex_document = create_open_vex_document(
            product_id=serializer.validated_data.get("product_id"),
            vulnerability_name=serializer.validated_data.get("vulnerability_name"),
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            author=serializer.validated_data.get("author"),
            role=serializer.validated_data.get("role"),
        )

        if not open_vex_document:
            return Response(status=HTTP_204_NO_CONTENT)

        response = HttpResponse(
            content=_object_to_json(open_vex_document),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=openvex_"
            + open_vex_document.get_base_id()
            + "_"
            + str(open_vex_document.version)
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
            content=_object_to_json(open_vex_document),
            content_type="text/json",
        )
        response["Content-Disposition"] = (
            "attachment; filename=openvex_"
            + open_vex_document.get_base_id()
            + "_"
            + str(open_vex_document.version)
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


def _object_to_json(object_to_encode: Any) -> str:
    json_string = jsonpickle.encode(object_to_encode, unpicklable=False)
    json_dict = json.loads(json_string)
    json_dict = _remove_empty_elements(json_dict)
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
