from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainDash, name='dd_mainDash'),
]