from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.item, name='item'),
    url(r'^item/rate/$', views.rate, name='rate'),
    url(r'^item/search/$', views.search, name='search'),
    url(r'^item/feedback/$', views.feedback, name='feedback'),
    url(r'^item/recommends/$', views.recommends, name='recommends'),
    url(r'^item/(?P<item_id>\d+)/$', views.item, name='item'),
    url(r'^(?P<e>c(ompany|reator|ategory))s/$', views.entity, name='entitys'),
    url(r'^(?P<e>c(ompany|reator|ategory))/(?P<e_id>\d+)$',
        views.entity, name='entity'),
]
