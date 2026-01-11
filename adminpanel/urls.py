from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.dashboard, name='admin_dashboard'),
    path('doctor-requests/', views.doctor_requests, name='doctor_requests'),
    path('approve-doctor/<int:pk>/', views.approve_doctor, name='approve_doctor'),
    path('reject-doctor/<int:pk>/', views.reject_doctor, name='reject_doctor'),

    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/', views.view_user, name='view_user'),
    path('users/<int:pk>/deactivate/', views.deactivate_user, name='deactivate_user'),

    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/<int:pk>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:pk>/remove/', views.remove_doctor, name='remove_doctor'),
    path('doctors/<int:pk>/remedies/', views.doctor_remedies, name='doctor_remedies'),

    path('plants/', views.manage_plants, name='manage_plants'),
    path('plants/add/', views.add_plant, name='add_plant'),
    path('plants/<int:pk>/edit/', views.edit_plant, name='edit_plant'),
    path('plants/<int:pk>/delete/', views.delete_plant, name='delete_plant'),

    path('remedies/', views.manage_remedies, name='manage_remedies'),
    path('remedies/add/', views.add_remedy, name='add_remedy'),
    path('remedies/<int:pk>/edit/', views.edit_remedy, name='edit_remedy'),
    path('remedies/<int:pk>/delete/', views.delete_remedy, name='delete_remedy'),

    path('consultations/', views.consultations_list, name='consultations_list'),

    path('dataset/', views.dataset_management, name='dataset_management'),
]
