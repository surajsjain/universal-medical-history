from django.urls import path
from . import views

urlpatterns = [
    path('', views.todayAppointments, name='dd_mainDash'),
    path('all_appointments/', views.allAppointments, name='all_appointments'),
    path('medical_history/', views.medicalHistory, name='patient_medical_history'),
]