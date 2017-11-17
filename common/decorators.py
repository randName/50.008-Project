from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from . import db


def json_response(func):
    """Decorator to respond with JSON from a request."""

    def decorator(request, *args, **kwargs):
        status = 500

        try:
            data = func(request, *args, **kwargs)
            status = 200
        except PermissionDenied:
            data = {'error': 'Forbidden'}
            status = 403
        except db.DatabaseError as e:
            data = db.error_to_dict(e)

        if isinstance(data, JsonResponse):
            return data

        if not isinstance(data, dict):
            data = {'data': data}

        return JsonResponse(data, status=status)

    return decorator
