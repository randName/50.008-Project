from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.admin, name='admin'),
    url(r'^new/$', views.new, name='new'),
    url(r'^stock/$', views.stock, name='stock'),
    url(r'^stats/(?P<entity>[a-z]+)/$', views.stats, name='stats'),
]
