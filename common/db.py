from django.db import connection, DatabaseError


def sql(query, *params):
    """Get rows from raw SQL query."""
    with connection.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def error_to_dict(error):
    return {
        'code': error.args[0],
        'error': type(error).__name__,
        'message': ' '.join(error.args[1:]),
    }


def page(page=1, per_page=20, sort=None):
    """Translate pagination parameters to SQL."""
    def des(s): return "%s DESC" % s[1:] if s[0] == '-' else s

    if sort:
        order = ' ORDER BY %s' % ', '.join(des(s) for s in sort)
    else:
        order = ''

    if per_page:
        pg = ' LIMIT %d OFFSET %d' % (per_page, (page-1)*per_page)
    else:
        pg = ''

    return order + pg
