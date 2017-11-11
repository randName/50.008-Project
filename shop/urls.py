from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^item/rate/$', views.rate, name='rate'),
    url(r'^item/search/$', views.search, name='search'),
    url(r'^item/feedback/$', views.feedback, name='feedback'),
    url(r'^item/recommends/$', views.recommends, name='recommends'),
    url(r'^item/(?P<item_id>\d+)/$', views.item, name='item'),
]
