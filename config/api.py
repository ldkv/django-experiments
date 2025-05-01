from django.conf import settings
from django.http import HttpRequest, JsonResponse


def debug(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "version": settings.VERSION,
            "environment": settings.ENV,
            "user": request.user.username,
        }
    )
