from django.urls import path
from . import views

app_name = 'patent_search'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_patent, name='search_patent'),
]