from django.conf.urls import url

from . import views

app_name = 'main'

urlpatterns = [
    # /main
    url(r'^$', views.index, name='index'),
    url(r'^process/', views.process, name='process'),
]
