from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainDash, name='ud_mainDash'),
    path('prev_visits/', views.prev_visits, name='ud_prev_visits'),
    path('doctor_search/', views.doctor_search, name='doc_search'),
    path('doctor_search/<int:doctor_id>/', views.book_visit, name='doc_details'),
]