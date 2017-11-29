from json import loads

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from common.db import sql, page
from common.utils import pagination
from common.messages import NOT_STAFF
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
        raise PermissionDenied(NOT_STAFF)

    s = """INSERT INTO item (id, name)
            VALUES (DEFAULT, %s)"""
    try:
        rq = loads(request.body)
        # sanitize before inserting
        values = (rq['name'],)
    except (ValueError, KeyError):
        return None

    sql(s, *values)

    return {}


@json_response
def stock(request, item_id):
    """Get or update current stock."""
    if not request.user.is_staff:
        raise PermissionDenied(NOT_STAFF)

    q = 'SELECT id, price, quantity FROM item WHERE id = %s'

    if request.method == 'POST':
        # update price and/or quantity from post data
        s = """UPDATE item SET
                quantity = %s
                WHERE id = %s"""
        try:
            rq = loads(request.body)
            # sanitize before inserting
            values = (int(rq['quantity']),)
        except (ValueError, KeyError):
            return None

        sql(s, *values, item_id)

    try:
        r = sql(q, item_id)[0]
    except IndexError:
        raise Http404

    return {
        'id': r[0],
        'price': r[1],
        'quantity': r[2],
    }


@json_response
def stats(request, entity, year, month):
    """Get stats for entity."""
    if not request.user.is_staff:
        raise PermissionDenied(NOT_STAFF)

    if entity not in ('item', 'company', 'creator'):
        raise Http404

    q = """SELECT item_id, SUM(quantity) AS total FROM purchase_item
            INNER JOIN purchase p ON p.id = purchase_item.purchase_id
            WHERE YEAR(p.made_on) = %s AND MONTH(p.made_on) = %s
            GROUP BY item_id"""
    pg = pagination(request)
    pg['sort'].append('-total')

    return sql(q + page(**pg), year, month)
