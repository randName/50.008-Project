from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items$', views.item, name='item'),
    url(r'^search$', views.search, name='search'),
    url(r'^(?P<entity>\w+)$', views.entity, name='entity'),
    url(r'^item/(?P<item_id>\d+)$', views.item, name='item'),
    url(r'^rate/(?P<item_id>\d+)$', views.rate, name='rate'),
    url(r'^feedback/(?P<item_id>\d+)$', views.feedback, name='feedback'),
    url(r'^recommends/(?P<item_id>\d+)$', views.recommends, name='recommends'),
    url(r'^(?P<entity>\w+)/(?P<entity_id>\d+)$', views.entity, name='entity'),
]
