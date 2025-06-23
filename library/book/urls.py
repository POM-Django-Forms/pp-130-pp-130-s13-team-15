from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_create'),
    path('<int:book_id>/edit/', views.book_update, name='book_update'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
]
