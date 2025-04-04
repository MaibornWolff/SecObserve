from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def empty_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(status=204)
