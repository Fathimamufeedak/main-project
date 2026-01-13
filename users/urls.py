from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('auth/', views.auth_select, name='auth_select'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/register/', views.register, name='user_register'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('search-remedies/', views.search_remedies, name='search_remedies'),
]
