from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from common.decorators import json_response


@require_POST
@login_required
@json_response
def submit(request):
    """Inserts order into database."""
    return {}


@login_required
@json_response
def order(request, order_id):
    """Get details of an order."""
    return {}
