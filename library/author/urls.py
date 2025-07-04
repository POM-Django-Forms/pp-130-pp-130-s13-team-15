# author/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list, name='author_list'),
    path('add/', views.author_create, name='author_create'),
    path('<int:author_id>/edit/', views.author_update, name='author_update'),
    path('<int:author_id>/delete/', views.author_delete, name='author_delete'),
    path('<int:author_id>/', views.author_detail, name='author_detail'),
]
