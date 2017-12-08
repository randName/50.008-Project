from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cart$', views.cart, name='cart'),
    url(r'^submit$', views.submit, name='submit_order'),
    url(r'^(?P<order_id>\d+)/$', views.order, name='order'),
]
