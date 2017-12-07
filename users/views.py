from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from orders.views import order
from common.db import sql, page
from common.utils import pagination, obj
from common.messages import NOT_LOGGED_IN
from common.decorators import json_response


def registration(request):
    """Registration page for new users."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@json_response
def alogin(request):
    """AJAX login/registration."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if not form.is_valid():
            errors = [' '.join(v) for v in form.errors.values()]
            raise ValidationError(errors)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

    return details(request)


@json_response
def details(request):
    """Get user details."""
    keys = ('id', 'is_authenticated', 'is_staff', 'date_joined',
            'username', 'email', 'first_name', 'last_name')
    return {k: getattr(request.user, k, None) for k in keys}


@json_response
def orders(request):
    """Get order history of logged-in user."""
    if not request.user.is_authenticated:
        raise PermissionDenied(NOT_LOGGED_IN)

    q = 'SELECT id, made_on, total FROM purchase WHERE user_id = %s'
    pg = pagination(request)

    for row in sql(q + page(**pg), request.user.id):
        yield order.__wrapped__(request, details=row)


@json_response
def feedbacks(request):
    """Get feedback made by logged-in user."""
    if not request.user.is_authenticated:
        raise PermissionDenied(NOT_LOGGED_IN)
    keys = ('item.id', 'item.name', 'score', 'review', 'made_on')
    q = """SELECT item_id, name, score, review, made_on
            FROM feedback INNER JOIN item
            ON item.id = feedback.item_id
            WHERE user_id = %s"""

    pg = pagination(request)

    for row in sql(q + page(**pg), request.user.id):
        yield obj(row, keys)


@json_response
def ratings(request):
    """Get feedback rated by logged-in user."""
    if not request.user.is_authenticated:
        raise PermissionDenied(NOT_LOGGED_IN)
    keys = ('item.id', 'item.name', 'user.id', 'user.username',
            'score', 'review', 'made_on', 'usefulness')
    q = """SELECT i.id, i.name, u.id, u.username,
            score, review, made_on, usefulness
            FROM rating r INNER JOIN feedback f
            ON r.item_id = f.item_id AND r.user_id = f.user_id
            INNER JOIN auth_user u ON r.user_id = u.id
            INNER JOIN item i ON r.item_id = i.id
            WHERE rater_id = %s"""

    pg = pagination(request)
    pg['sort'].append('-usefulness')

    for row in sql(q + page(**pg), request.user.id):
        yield obj(row, keys)
