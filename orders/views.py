from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from common.db import sql
from common.decorators import json_response
from common.messages import NOT_LOGGED_IN, WRONG_ACCOUNT


@require_POST
@json_response
def submit(request):
    """Inserts order into database."""
    if not request.user.is_authenticated:
        raise PermissionDenied(NOT_LOGGED_IN)

    return {}


@json_response
def order(request, order_id=None, details=None):
    """Get details of an order."""

    if details is None:
        q = 'SELECT user_id, made_on, total FROM purchase WHERE id = %s'
        try:
            uid, made_on, total = sql(q, order_id)[0]
        except IndexError:
            return None

        if uid != request.user.id:
            raise PermissionDenied(WRONG_ACCOUNT)
    else:
        order_id, made_on, total = details

    q = """SELECT item_id, name, p.quantity
            FROM purchase_item p INNER JOIN item
            ON p.item_id = item.id
            WHERE purchase_id = %s"""

    items = tuple({
        'id': iid,
        'name': name,
        'quantity': qty,
    } for iid, name, qty in sql(q, order_id))

    return {
        'id': order_id,
        'total': total,
        'items': items,
        'made_on': made_on,
    }
