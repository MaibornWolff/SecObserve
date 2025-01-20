from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from application.access_control.services.authorization import user_has_permission
from application.access_control.services.roles_permissions import Permissions
from application.core.queries.product import get_product_by_id
from application.osv.services.osv_scanner import scan_product


class ScanOSVProductView(APIView):
    @action(detail=True, methods=["post"])
    def post(self, request, product_id: int):
        product = get_product_by_id(product_id)
        if not product:
            return Response(status=HTTP_404_NOT_FOUND)
        if not user_has_permission(product, Permissions.Product_Scan_OSV):
            return Response(status=HTTP_404_NOT_FOUND)

        scan_product(product)

        return Response(status=HTTP_204_NO_CONTENT)
