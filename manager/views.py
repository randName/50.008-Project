from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from common.messages import NO_PERMISSION
from common.decorators import json_response


@login_required
def admin(request):
    """Show main admin page."""
    if not request.user.is_staff:
        return render(request, 'manager/denied.html')
    return render(request, 'manager/index.html')


@require_POST
@json_response
def new(request):
    """Add item or entity into inventory."""
    if not request.user.is_staff:
        return NO_PERMISSION
    return {}


@json_response
def stock(request):
    """Get or update current stock."""
    if not request.user.is_staff:
        return NO_PERMISSION
    return {}


@json_response
def stats(request, entity=None):
    """Get stats for entity."""
    if not request.user.is_staff:
        return NO_PERMISSION
    return {}
