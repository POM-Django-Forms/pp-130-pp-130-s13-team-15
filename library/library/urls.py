from django.contrib import admin
from django.urls import path
from authentication import views as auth_views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.home_view, name='home'),
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('books/', include('book.urls')),
    path('orders/',  include('order.urls')),
    path('authors/', include('author.urls')),
    path('users/',            auth_views.user_list,   name='user_list'),
    path('users/<int:user_id>/', auth_views.user_detail, name='user_detail'),
]
