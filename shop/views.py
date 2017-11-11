from django.shortcuts import render

from common.decorators import json_response


def index(request):
    """Main page of site."""
    return render(request, 'shop/index.html')


@json_response
def item(request, item_id):
    """Get item details."""
    return {}


@json_response
def search(request):
    """Search for item."""
    return {}


@json_response
def feedback(request):
    """Get or submit feedback for item."""
    return {}


@json_response
def rate(request):
    """Get or submit rating for feedback."""
    return {}


@json_response
def recommends(request):
    """Get recommended items."""
    return {}
