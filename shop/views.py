from django.shortcuts import render

from common.db import sql, page
from common.utils import pagination
from common.decorators import json_response


def index(request):
    """Main page of site."""
    return render(request, 'shop/index.html')


@json_response
def entity(request, e, e_id=None):
    """Get entity details."""
    if e_id:
        q = 'SELECT name FROM {} WHERE id = %s'.format(e)
        try:
            return {
                'id': e_id,
                'name': sql(q, int(e_id))[0][0],
            }
        except IndexError:
            return None

    q = 'SELECT id, name FROM {}'.format(e)
    pg = pagination(request)

    return ({'id': i[0], 'name': i[1]} for i in sql(q + page(**pg)))


@json_response
def item(request, item_id=None):
    """Get item details."""
    if item_id:
        q = """SELECT name, price, quantity, description, date_created, company_id
                FROM item WHERE id = %s"""
        try:
            it = sql(q, item_id)[0]
        except IndexError:
            return None

        q = """SELECT {0}.id, {0}.name FROM item_{0}
                INNER JOIN {0} ON item_{0}.{0}_id = {0}.id
                WHERE item_id = %s"""
        cs = {}
        for k in ('creator', 'category'):
            c = sql(q.format(k), item_id)
            cs[k+'s'] = tuple({'id': i[0], 'name': i[1]} for i in c)

        return {
            **cs,
            'id': item_id,
            'name': it[0],
            'price': it[1],
            'quantity': it[2],
            'description': it[3],
            'date_created': it[4],
            'company': entity.__wrapped__(None, 'company', it[5]),
        }

    q = 'SELECT id, name FROM item'
    pg = pagination(request)

    return ({'id': i[0], 'name': i[1]} for i in sql(q + page(**pg)))


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
