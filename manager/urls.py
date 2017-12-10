from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new$', views.new, name='new'),
    url(r'^stock/(?P<item_id>\d+)$', views.stock, name='stock'),
    url(r'^stats/(?P<entity>\w+)/(?P<year>\d{4})/(?P<month>\d+)$',
        views.stats, name='stats'),
]
