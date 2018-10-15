from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sale_list, name='sale_list'),
]