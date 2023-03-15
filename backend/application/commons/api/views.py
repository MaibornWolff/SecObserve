from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from application.commons.api.serializers import CommitSerializer


class StatusView(APIView):

    serializer_class = CommitSerializer

    @action(detail=True, methods=["get"], url_name="commit_id")
    def get(self, request, format=None):
        content = {
            "commit_id": "placeholder",
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
