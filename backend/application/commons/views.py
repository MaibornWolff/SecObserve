from django.http import HttpResponse


def empty_view(request):
    return HttpResponse(status=204)
