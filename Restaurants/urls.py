from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'), #Homepage
    url(r'^search', views.search, name = 'search') #Search page
]
