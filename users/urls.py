from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^orders/$', views.orders, name='api.orders'),
    url(r'^ratings/$', views.ratings, name='api.ratings'),
    url(r'^feedbacks/$', views.feedbacks, name='api.feedbacks'),
    url(r'^register/$', views.registration, name='registration'),
]
