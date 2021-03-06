from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items$', views.item, name='item'),
    url(r'^search$', views.search, name='search'),
    url(r'^entities$', views.entity, name='entity'),
    url(r'^item/(?P<item_id>\d+)$', views.item, name='item'),
    url(r'^feedback/(?P<item_id>\d+)$', views.feedback, name='feedback'),
    url(r'^rate/(?P<item_id>\d+)/(?P<user_id>\d+)$', views.rate, name='rate'),
    url(r'^recommends/(?P<item_id>\d+)$', views.recommends, name='recommends'),
]
