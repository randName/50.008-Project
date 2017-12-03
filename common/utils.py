def pagination(request, defaults=(1, 20)):
    """Get pagination parameters from request."""
    if request is None:
        return {'sort': []}

    p = {}

    try:
        p['per_page'] = int(request.GET.get('per_page'))
        p['page'] = int(request.GET.get('page'))
    except (TypeError, ValueError):
        pass

    sort = request.GET.get('sort', '').split(',')

    if sort[0]:
        p['sort'] = sort
    else:
        p['sort'] = []

    return p


def obj(values, keys=('id', 'name')):
    n = {}
    nested = tuple(i for i in reversed(range(len(keys))) if '.' in keys[i])
    if nested:
        keys = list(keys)
        values = list(values)
        for i in nested:
            k, sk = keys.pop(i).split('.')
            if k not in n:
                n[k] = {}
            n[k][sk] = values.pop(i)
        for k, v in n.items():
            n[k] = obj(v.values(), tuple(v.keys()))
    return dict(zip(keys, values), **n)
