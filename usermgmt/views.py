from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    else:
        pass