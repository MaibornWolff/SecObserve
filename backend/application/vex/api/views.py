import json
from typing import Any

import jsonpickle
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from application.vex.api.serializers import (
    OpenVEXDocumentCreateSerializer,
    OpenVEXDocumentUpdateSerializer,
)
from application.vex.services.open_vex import (
    create_open_vex_document,
    update_open_vex_document,
)


class OpenVEXDocumentCreateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentCreateSerializer,
        responses={200: None},
    )
    @action(detail=False, methods=["post"])
    def post(self, request):
        serializer = OpenVEXDocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        open_vex_document = create_open_vex_document(
            product_id=serializer.validated_data.get("product_id"),
            vulnerability_name=serializer.validated_data.get("vulnerability_name"),
            document_id_prefix=serializer.validated_data.get("document_id_prefix"),
            author=serializer.validated_data.get("author"),
        )

        response = HttpResponse(
            content=_object_to_json(open_vex_document),
            content_type="text/json",
        )
        response["Content-Disposition"] = "attachment; filename=openvex.json"
        return response


class OpenVEXDocumentUpdateView(APIView):
    @extend_schema(
        methods=["POST"],
        request=OpenVEXDocumentUpdateSerializer,
        responses={200: None, 201: None},
    )
    @action(detail=False, methods=["post"])
    def post(self, request):
        serializer = OpenVEXDocumentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        open_vex_document = update_open_vex_document(
            document_id=serializer.validated_data.get("document_id"),
            author=serializer.validated_data.get("author"),
        )

        if not open_vex_document:
            return Response(status=201)

        response = HttpResponse(
            content=_object_to_json(open_vex_document),
            content_type="text/json",
        )
        response["Content-Disposition"] = "attachment; filename=openvex.json"
        return response


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
