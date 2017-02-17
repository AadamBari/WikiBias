from django.conf.urls import url
from . import views # . means current directory

app_name = 'analysis'

urlpatterns = [
    # /analysis
    url(r'^$', views.index, name='index'),
]
