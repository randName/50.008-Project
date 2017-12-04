from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.alogin, name='login'),
    url(r'^orders$', views.orders, name='user.orders'),
    url(r'^details$', views.details, name='user.details'),
    url(r'^ratings$', views.ratings, name='user.ratings'),
    url(r'^feedbacks$', views.feedbacks, name='user.feedbacks'),
]
