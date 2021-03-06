from json import loads

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from common.db import sql
from common.utils import obj
from common.decorators import json_response
from common.messages import NOT_LOGGED_IN, WRONG_ACCOUNT


@json_response
def cart(request):
    """Get or update session cart."""
    ses_cart = request.session.get('cart', {})

    if request.method == 'POST':
        try:
            rq = loads(request.body)
            i = int(rq['id'])
            q = int(rq['quantity'])
            if q > 0:
                ses_cart[str(i)] = {
                    'id': i,
                    'quantity': q,
                    'name': rq['name'],
                    'price': float(rq['price']),
                }
            else:
                ses_cart.pop(str(i), None)
            request.session['cart'] = ses_cart
        except (ValueError, KeyError):
            pass

    return (i for i in ses_cart.values())


@require_POST
@json_response
def submit(request):
    """Inserts order into database."""
    if not request.user.is_authenticated:
        raise PermissionDenied(NOT_LOGGED_IN)
    q = 'SELECT price FROM item WHERE id = %s'
    sp = """INSERT INTO purchase (id, made_on, user_id, total)
            VALUES (DEFAULT, NOW(), %s, %s)"""
    si = """INSERT INTO purchase_item (purchase_id, item_id, quantity)
            VALUES (%s, %s, %s)"""
    uid = request.user.id
    pid = None
    items = []
    total = 0
    try:
        rq = loads(request.body)
        for item in rq['order']:
            iid = int(item['id'])
            qty = int(item['quantity'])
            try:
                total += qty*sql(q, iid)[0][0]
                items.append((iid, qty))
            except IndexError:
                pass
    except (ValueError, KeyError):
        return {}

    if items:
        pid = sql(sp, uid, total)
        for iid, qty in items:
            sql(si, pid, iid, qty)

    request.session.pop('cart', None)
    return {'id': pid, 'total': total}


@json_response
def order(request, order_id=None, details=None):
    """Get details of an order."""

    if details is None:
        q = 'SELECT user_id, made_on, total FROM purchase WHERE id = %s'
        try:
            uid, made_on, total = sql(q, order_id)[0]
        except IndexError:
            return Http404

        if uid != request.user.id:
            raise PermissionDenied(WRONG_ACCOUNT)
    else:
        order_id, made_on, total = details

    keys = ('id', 'name', 'quantity')
    q = """SELECT item_id, name, p.quantity FROM purchase_item p
            INNER JOIN item ON p.item_id = item.id
            WHERE purchase_id = %s"""

    return {
        'id': order_id,
        'total': total,
        'made_on': made_on,
        'items': tuple(obj(i, keys) for i in sql(q, order_id)),
    }
