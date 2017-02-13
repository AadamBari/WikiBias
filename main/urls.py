from django.conf.urls import url

from . import views

urlpatterns = [
    # /main
    url(r'^$', views.index, name='index'),
]