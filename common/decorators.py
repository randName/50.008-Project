from django.http import JsonResponse


def json_response(func):
    """Decorator to respond with JSON from a request."""

    def decorator(request, *args, **kwargs):
        data = func(request, *args, **kwargs)
        if isinstance(data, JsonResponse):
            return data
        return JsonResponse(data)

    return decorator
