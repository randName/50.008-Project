from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from common.db import sql, page
from common.utils import pagination
from common.decorators import json_response
from common.messages import NOT_LOGGED_IN

import datetime


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
    q = """SELECT item.name, item.id, item.company_id, item.description, item.price, item.quantity, item.date_created, item_creator.creator_id, item_category.category_id, feedback.avg_score
                FROM item, item_creator, item_category WHERE item.id = item_category.id AND item.id = item_creator.id"""
    q1 = """name = {0}""".format(request.name)
    q2 = """company_id = {0}""".format(request.company_id)
    q3 = """category_id = {0}""".format(request.category_id)
    q4 = """creator_id = {0}""".format(request.creator_id)
    q5 = """ORDER BY item.date_created"""
    q6 = """ORDER BY avg_score"""
    q7 = """UNION (SELECT AVERAGE(score) AS avg_score FROM feedback GROUP BY item_id)"""
    if request.name == 'None':
        q1 = """"""
    elif request.company_id == 'None':
        q2 = """"""
    elif request.category_id == 'None':
        q3 = """"""
    elif request.creator_id == 'None':
        q4 = """"""
    elif request.sortmethod == 'year':
        q6 = """"""
    elif request.sortmethod == 'avergae score':
        q5 = """"""

    q = q+ """AND""" + q1 +  """AND""" + q2 + """AND""" + q3 + """AND""" + q4 + """AND"""+ q7 + q5 + q6
    pg = pagination(request)
    for it in sql(q+page(**pg)):
        yield {
            'name': it[0],
            'id': it[1],
            'company_id': it[2],
            'description': it[3],
            'price': it[4],
            'quantity': it[5],
            'date_created': it[6],
            'creator_id': it[7],
            'category_id': it[8],
            'average_score': it[9]
        }

@json_response
def feedback(request):
    """Get or submit feedback for item."""
    # use username and bookname as input
    q = """SELECT id FROM auth_user WHERE username = {}""".format(request.username)
    pg = pagination(request)
    try:
        user_id = sql(q + page(**pg))[0][0]
    except:
        return None
    q = """SELECT id FROM item WHERE name = {}""".format(request.bookname)
    try:
        book_id = sql(q + page(**pg))[0][0]
    except:
        return None
    if request.func=='get':
        q = """SELECT review FROM feedback WHERE user_id = {0} AND item_id = {1}""".format(user_id,book_id)
        for row in sql(q + page(**pg)):
            yield {
                'review': row[0]
            }
    else:
        q = """INSERT INTO feedback (item_id, user_id, score, review, made_on) VALUES ({0},{1},{2},{3},{4})""".format(book_id,user_id,request.score,request.review,datetime.datetime.now())
        sql(q+page(**pg))
        return None



@json_response
def rate(request):
    """Get or submit rating for feedback."""
    # use username and bookname as input
    q = """SELECT id FROM auth_user WHERE username = {}""".format(request.username)
    pg = pagination(request)
    try:
        user_id = sql(q + page(**pg))[0][0]
    except:
        return None
    q = """SELECT id FROM item WHERE name = {}""".format(request.bookname)
    try:
        book_id = sql(q + page(**pg))[0][0]
    except:
        return None
    q = """SELECT id FROM auth_user WHERE username = {}""".format(request.ratername)
    pg = pagination(request)
    try:
        rater_id = sql(q + page(**pg))[0][0]
    except:
        return None
    if request.func == 'get':
        q = """SELECT review FROM feedback WHERE user_id = {0} AND item_id = {1} AND rater_id ={2}""".format(user_id, book_id, rater_id)

        for row in sql(q + page(**pg)):
            yield {
                'review': row[0]
            }
    else:
        q = """INSERT INTO rating (item_id, user_id, rater_id, usefulness) VALUES ({0},{1},{2},{3})""".format(
            book_id, user_id, rater_id, request.usefulness)
        sql(q + page(**pg))
        return None


@json_response
def recommends(request):
    """Get recommended items."""
    q = """SELECT id FROM item WHERE name = {}""".format(request.bookname)
    pg = pagination(request)
    try:
        book_id = sql(q + page(**pg))[0][0]
    except:
        return None
    q = """SELECT review, user_name FROM (SELECT review, user_id FROM (SELECT review, AVG(usefulness) as score, user_id FROM rating WHERE item_id = {0} GROUP BY user_id) ORDER BY score LIMIT {1}), auth_user WHERE auth_user.id=user_id""".format(book_id, request.topn)
    pg = pagination(request)
    for row in sql(q + page(**pg)):
        yield {
            'review':row[0],
            'user_name':row[1]
        }
