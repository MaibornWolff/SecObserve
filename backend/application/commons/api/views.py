from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from application.commons.api.serializers import VersionSerializer


class VersionView(APIView):

    serializer_class = VersionSerializer

    @action(detail=True, methods=["get"], url_name="version")
    def get(self, request, format=None):
        content = {
            "version": "unkown",
        }
        return Response(content)


class HealthView(APIView):

    authentication_classes = []
    permission_classes = []
    serializer_class = None

    @action(detail=True, methods=["get"], url_name="health")
    def get(self, request, format=None):
        response = Response()
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"

        return response
