from json import loads

from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from common.db import sql, page
from common.utils import pagination
from common.messages import NOT_LOGGED_IN
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
    q = """SELECT id, name, score, date_created FROM item
            LEFT JOIN (SELECT item_id, AVG(score) AS score FROM feedback
                GROUP BY item_id) f ON item.id = f.item_id"""
    pg = pagination(request)

    for row in sql(q + page(**pg)):
        yield {
            'id': row[0],
            'name': row[1],
            'score': row[2],
            'date_created': row[3],
        }


@json_response
def feedback(request):
    """Get or submit feedback for item."""
    q = """SELECT score, review, made_on, user_id, username, item_id, name
            FROM feedback
            INNER JOIN auth_user ON feedback.user_id = auth_user.id
            INNER JOIN item ON feedback.item_id = item.id
            WHERE item_id = %s"""

    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        pg = pagination(request)

        return sql(q + page(**pg), item_id)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied(NOT_LOGGED_IN)
        uid = request.user.id

        s = """INSERT INTO feedback (user_id, item_id, score, review, made_on)
                VALUES (%s, %s, %s, %s, NOW())"""
        try:
            rq = loads(request.body)
            values = tuple(rq[k] for k in ('item_id', 'score', 'review'))
        except (ValueError, KeyError):
            return None

        sql(s, uid, *values)
        return sql(q + ' AND user_id = %s', rq['item_id'], uid)[0]


@json_response
def rate(request):
    """Get or submit rating for feedback."""
    if request.method == 'GET':
        q = """SELECT user_id, rater_id, usefulness FROM rating
                WHERE item_id = %s"""
        pg = pagination(request)
        pg['sort'].append('-usefulness')

        return sql(q + page(**pg))
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied(NOT_LOGGED_IN)
        uid = request.user.id

        s = """INSERT INTO rating (rater_id, item_id, user_id, usefulness)
                VALUES (%s, %s, %s, %s)"""
        try:
            rq = loads(request.body)
            values = tuple(rq[k] for k in ('item_id', 'user_id', 'usefulness'))
        except (ValueError, KeyError):
            return None

        sql(s, uid, *values)
        return None


@json_response
def recommends(request):
    """Get recommended items."""
    return {}
