from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainDash, name='ud_mainDash'),
    path('prev_visits/', views.prev_visits, name='ud_prev_visits'),
    path('prev_visits/<int:visit_id>/<int:viewer>/', views.visit_details, name='visit_details'), #Viewer: 0 for user and 1 for doctor
    path('doctor_search/', views.doctor_search, name='doc_search'),
    path('doctor_search/<int:doctor_id>/', views.book_visit, name='doc_details'),
]