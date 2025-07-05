from django.urls import path
from . import views

app_name = 'patent_search'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_patent, name='search_patent'),
    path('opd/documents/', views.get_opd_documents, name='get_opd_documents'),
    path('opd/jp-text/', views.get_jp_document_text, name='get_jp_document_text'),
]