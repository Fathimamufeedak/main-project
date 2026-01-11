from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_consultation, name='upload_consultation'),
    path('my/', views.user_consultations, name='user_consultations'),
    path('<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('<int:pk>/edit/', views.edit_consultation, name='edit_consultation'),
    path('<int:pk>/delete/', views.delete_consultation, name='delete_consultation'),
]
