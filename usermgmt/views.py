from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

# Create your views here.
def login(request):
    if request.method == 'GET':
        if(request.user.is_authenticated):
            # TODO: Check the user type (Doctor or Regular user) and redirect accordingly
            return redirect('ud_mainDash')
        else:
            return render(request, 'auth/login.html')

    elif request.method == 'POST':
        data = request.POST

        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth.login(request, user)
                return redirect('ud_mainDash') # TODO: Check the user type (Doctor or Regular user) and redirect accordingly
            else:
                return redirect('login')

        except:
            print('could not get the user')
            return redirect('login')

def logout(request):
    if(request.method == 'POST'):
        auth.logout(request)
        return redirect('login')