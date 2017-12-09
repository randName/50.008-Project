from json import loads

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from common.db import sql, page
from common.messages import NOT_STAFF
from common.utils import pagination, obj
from common.decorators import json_response


@require_POST
@json_response
def new(request):
    """Add item or entity into inventory."""
    if not request.user.is_staff:
        raise PermissionDenied(NOT_STAFF)
    values = []
    m2m = {'category': [], 'creator': []}
    sc = 'INSERT INTO item_{0} (item_id, {0}_id) VALUES (%s, %s)'
    si = """INSERT INTO item (id, name, description, date_created,
            company_id, quantity, price)
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"""
    try:
        rq = loads(request.body)
        values.extend(rq[k] for k in ('name', 'description', 'date'))
        values.extend(int(rq[k]) for k in ('company', 'quantity'))
        values.append(float(rq['price']))
        for k, v in m2m.items():
            for c in rq.get(k, ()):
                try:
                    v.append(int(c))
                except ValueError:
                    pass
    except (ValueError, KeyError):
        return {}

    iid = sql(si, *values)
    for k, v in m2m.items():
        for i in v:
            sql(sc.format(k), iid, i)

    return {'id': iid}


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
        return obj(sql(q, item_id)[0], ('id', 'price', 'quantity'))
    except IndexError:
        raise Http404


@json_response
def stats(request, entity, year, month):
    """Get stats for entity."""
    if not request.user.is_staff:
        raise PermissionDenied(NOT_STAFF)

    if entity not in ('item', 'company', 'creator'):
        raise Http404

    keys = ('%s.id' % entity, '%s.name' % entity, 'total')
    sqs = {
        'item': ('', 'item.id'),
        'company': ('INNER JOIN item ON company.id = item.company_id',
                    'item.id'),
        'creator': (
            'INNER JOIN item_creator ON creator.id = item_creator.creator_id',
            'item_creator.item_id'
        )
    }
    q = """SELECT {0}.id, {0}.name, SUM(purchase_item.quantity) AS total
            FROM {0} {1}
            INNER JOIN purchase_item ON purchase_item.item_id = {2}
            INNER JOIN purchase p ON p.id = purchase_item.purchase_id
            WHERE YEAR(p.made_on) = %s AND MONTH(p.made_on) = %s
            GROUP BY {0}.id""".format(entity, *sqs[entity])

    pg = pagination(request)
    pg['sort'].append('-total')
    return (obj(i, keys) for i in sql(q + page(**pg), year, month))
