from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_doctor, name='doctor_register'),
    path('login/', views.doctor_login, name='doctor_login'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('consultations/', views.consultation_list, name='doctor_consultations'),
    path('consultation/<int:pk>/', views.consultation_detail, name='doctor_consultation_detail'),
    path('consultation/<int:pk>/remedy/', views.remedy_form, name='doctor_remedy_form'),
    path('remedies/add/', views.doctor_add_remedy, name='doctor_add_remedy'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
]
