from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_doctor, name='doctor_register'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
