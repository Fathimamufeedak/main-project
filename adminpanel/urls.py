from django.urls import path
from . import views

urlpatterns = [
    path('doctor-requests/', views.doctor_requests, name='doctor_requests'),
    path('approve-doctor/<int:pk>/', views.approve_doctor, name='approve_doctor'),
    path('dataset/', views.dataset_placeholder, name='dataset_placeholder'),
]
