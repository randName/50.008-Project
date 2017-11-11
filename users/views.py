from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
    return {}


@json_response
def feedbacks(request):
    """Get feedback made by logged-in user."""
    if not request.user.is_authenticated:
        return NOT_LOGGED_IN
    return {}


@json_response
def ratings(request):
    """Get feedback rated by logged-in user."""
    if not request.user.is_authenticated:
        return NOT_LOGGED_IN
    return {}
