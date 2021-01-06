from django.urls import path
from . import views

urlpatterns = [
    path('', views.todayAppointments, name='dd_mainDash'),
    path('all_appointments/', views.allAppointments, name='all_appointments'),
    path('all_appointments/<int:visit_id>/', views.appointmentFilling, name='visit_filling'),
    path('all_appointments/<int:visit_id>/prescriptions', views.appointmentFilling, name='prescription_filling'),
    path('medical_history/', views.medicalHistory, name='patient_medical_history'),
    path('medical_history/<int:patient_id>/', views.medicalProfile, name='medical_profile'),
]