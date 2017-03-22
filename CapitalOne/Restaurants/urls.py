from django.conf.urls import url
#from django.views.generic import ListView, DetailView
#from Restaurants.models import Recommendation
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'), #Homepage
    #url(r'^Recommendations', ListView.as_view(queryset=Recommendation.objects.all().order_by("name")[:5], template_name = "Restaurants/Recommendations.html"))
    #Show top 5 restaurant objects fetched as models in alphabetical order
    url(r'^search', views.search, name = 'search')
]
