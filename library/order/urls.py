from django.urls import path
from . import views

urlpatterns = [
    path('',                views.order_list,   name='order_list'),   # все заказы (librarian)
    path('my/',             views.my_orders,    name='my_orders'),    # мои заказы (user)
    path('create/',         views.create_order, name='create_order'), # создать заказ (user)
    path('<int:order_id>/close/', views.close_order, name='close_order'),  # закрыть заказ (librarian)
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
