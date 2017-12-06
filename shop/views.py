from json import loads

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from common.db import sql, page
from common.utils import pagination, obj
from common.messages import NOT_LOGGED_IN
from common.decorators import json_response

m2m = ('creator', 'category')


def index(request):
    """Main page of site."""
    return render(request, 'shop/index.html')


@json_response
def entity(request):
    """Get entity details."""
    nq = request.GET.get('q')
    if not nq:
        return None

    q = 'SELECT id, name FROM {} WHERE LOWER(name) LIKE %s LIMIT 3'
    nq = '%' + nq.lower() + '%'

    results = []
    for e in ('company',) + m2m:
        results.extend({'type': e, **obj(i)} for i in sql(q.format(e), nq))
    return results


@json_response
def item(request, item_id=None):
    """Get item details."""
    keys = ('id', 'name', 'price', 'quantity', 'description', 'date_created',
            'company.id', 'company.name')

    if item_id:
        q = """SELECT item.id, item.name, price, quantity, description,
                date_created, company.id, company.name FROM item
                INNER JOIN company ON company.id = company_id
                WHERE item.id = %s"""
        try:
            it = obj(sql(q, item_id)[0], keys)
        except IndexError:
            raise Http404

        cq = """SELECT {0}.id, {0}.name FROM item_{0}
                INNER JOIN {0} ON item_{0}.{0}_id = {0}.id
                WHERE item_id = %s"""
        for k in m2m:
            it[k+'s'] = tuple(obj(i) for i in sql(cq.format(k), item_id))
        return it

    q = 'SELECT id, name FROM item'
    pg = pagination(request)
    return (obj(i) for i in sql(q + page(**pg)))


@json_response
def search(request):
    """Search for item."""
    q = """SELECT id, name, score, date_created FROM item
            LEFT JOIN (SELECT item_id, AVG(score) AS score FROM feedback
                GROUP BY item_id) f ON item.id = f.item_id"""
    pg = pagination(request)

    i = 'id IN (SELECT id FROM item {0} WHERE {1})'
    sq = ((' ', 'INNER JOIN item_{0} {0}{1} ON item.id = {0}{1}.item_id'),
          (' AND ', '{0}{1}.{0}_id = %s'))

    mfil = tuple(((k, i), v) for k in m2m for i, v in enumerate(
                   v for v in request.GET.get(k, '').split(',') if v))
    if mfil:
        ks, vs = zip(*mfil)
        vals = list(vs)
        fils = [i.format(*(j.join(s.format(*k) for k in ks) for j, s in sq))]
    else:
        vals = []
        fils = []

    cf = request.GET.get('company')
    try:
        vals.append(int(cf))
        fils.append('company_id = %s')
    except (TypeError, ValueError):
        pass

    nf = request.GET.get('name')
    if nf:
        vals.append('%' + nf.lower() + '%')
        fils.append('LOWER(name) LIKE %s')

    if fils:
        q += ' WHERE ' + ' AND '.join(fils)

    for row in sql(q + page(**pg), *vals):
        yield obj(row, ('id', 'name', 'score', 'date_created'))


@json_response
def feedback(request, item_id):
    """Get or submit feedback for item."""
    keys = ('score', 'review', 'made_on', 'usefulness',
            'user.id', 'user.username')
    q = """SELECT score, review, made_on, usefulness, f.user_id, username
            FROM feedback f
            INNER JOIN auth_user ON f.user_id = auth_user.id
            LEFT JOIN (SELECT item_id, user_id, AVG(usefulness) AS usefulness
                FROM rating GROUP BY item_id, user_id) r
                ON f.item_id = r.item_id AND f.user_id = r.user_id
            WHERE f.item_id = %s"""

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied(NOT_LOGGED_IN)
        uid = request.user.id

        s = """INSERT INTO feedback (user_id, item_id, score, review, made_on)
                VALUES (%s, %s, %s, %s, NOW())"""
        try:
            rq = loads(request.body)
            sql(s, uid, item_id, int(rq['score']), rq['review'])
            return obj(sql(q + ' AND user_id = %s', item_id, uid)[0], keys)
        except (ValueError, KeyError):
            return None

    pg = pagination(request)
    pg['sort'].append('-usefulness')
    return (obj(i, keys) for i in sql(q + page(**pg), item_id))


@json_response
def rate(request, item_id, user_id):
    """Get or submit rating for feedback."""
    q = """SELECT u FROM (SELECT item_id, user_id, AVG(usefulness) AS u
            FROM rating GROUP BY item_id, user_id) r
            WHERE item_id = %s AND user_id = %s"""

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied(NOT_LOGGED_IN)
        uid = request.user.id

        s = """INSERT INTO rating (rater_id, item_id, user_id, usefulness)
                VALUES (%s, %s, %s, %s)"""
        try:
            rq = loads(request.body)
            sql(s, uid, item_id, user_id, int(rq['usefulness']))
        except (ValueError, KeyError):
            pass
    try:
        return sql(q, item_id, user_id)[0][0]
    except IndexError:
        raise Http404


@json_response
def recommends(request, item_id):
    """Get recommended items."""
    keys = ('id', 'name', 'users', 'sales')
    q = """SELECT item.id, name, COUNT(DISTINCT p1.user_id) AS users,
                SUM(i1.quantity) AS sales FROM item
            INNER JOIN purchase_item i1 ON i1.item_id = id
            INNER JOIN purchase p1 ON i1.purchase_id = p1.id
            INNER JOIN purchase p2 ON p1.user_id = p2.user_id
            INNER JOIN purchase_item i2 ON i2.purchase_id = p2.id
                AND i1.item_id <> i2.item_id AND i2.item_id = %s
            GROUP BY item.id
            """
    pg = pagination(request)
    pg['sort'].append('-sales')
    return (obj(i, keys) for i in sql(q + page(**pg), item_id))
