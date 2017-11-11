from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from common.db import sql, page
from common.utils import pagination
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


@login_required
def profile(request):
    """Show profile of logged-in user."""
    return render(request, 'users/profile.html', {'user': request.user})


@json_response
def orders(request):
    """Get order history of logged-in user."""
    if not request.user.is_authenticated:
        return NOT_LOGGED_IN

    q = 'SELECT id, made_on, total FROM purchase WHERE user_id = %s'
    pg = pagination(request)

    return sql(q + page(**pg), request.user.id)


@json_response
def feedbacks(request):
    """Get feedback made by logged-in user."""
    if not request.user.is_authenticated:
        return NOT_LOGGED_IN

    q = 'SELECT item_id, made_on, score FROM feedback WHERE user_id = %s'
    pg = pagination(request)

    return sql(q + page(**pg), request.user.id)


@json_response
def ratings(request):
    """Get feedback rated by logged-in user."""
    if not request.user.is_authenticated:
        return NOT_LOGGED_IN

    q = """SELECT usefulness, r.item_id, r.user_id, score, review
            FROM rating r INNER JOIN feedback f
            ON r.item_id = f.item_id AND r.user_id = f.user_id
            WHERE rater_id = %s"""

    pg = pagination(request)
    pg['sort'].append('-usefulness')

    return sql(q + page(**pg), request.user.id)
