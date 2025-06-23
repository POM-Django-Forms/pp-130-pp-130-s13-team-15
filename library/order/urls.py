from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.order_list,   name='order_list'),
    path('my/',                 views.my_orders,    name='my_orders'),
    path('add/',                views.create_order, name='create_order'),
    path('<int:order_id>/',     views.order_detail, name='order_detail'),
    path('<int:order_id>/edit/',views.order_update, name='order_update'),
    path('<int:order_id>/close/',views.close_order, name='close_order'),
]
