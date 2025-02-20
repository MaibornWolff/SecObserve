from django.http import HttpRequest, HttpResponse


def empty_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(status=204)
