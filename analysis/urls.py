from django.conf.urls import url
from . import views # . means current directory



urlpatterns = [
    # /analysis
    url(r'^$', views.index, name = 'index'),
]
