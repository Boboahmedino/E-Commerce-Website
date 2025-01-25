from django.urls import path
from .import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('admin_user', views.admin_user, name = 'admin_user'),
    path('admin_logout', views.admin_logout, name = 'admin_logout'),

]