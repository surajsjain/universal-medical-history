from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

from .models import UserDetails

# Create your views here.
def login(request):
    if request.method == 'GET':
        if(request.user.is_authenticated):
            redirect_dest = 'ud_mainDash'
            u_det = UserDetails.objects.get(user=request.user)
            if(u_det.is_doctor):
                redirect_dest = 'dd_mainDash'

            return redirect(redirect_dest)


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

                redirect_dest = 'ud_mainDash'
                u_det = UserDetails.objects.get(user=user)
                if (u_det.is_doctor):
                    redirect_dest = 'dd_mainDash'

                return redirect(redirect_dest)
            else:
                return redirect('login')

        except:
            print('could not get the user')
            return redirect('login')



def logout(request):
    if(request.method == 'POST'):
        auth.logout(request)
        return redirect('login')

def signup(request):
    if(request.method == 'GET'):
        return render(request, 'auth/signup.html')

    elif(request.method == 'POST'):
        data = request.POST

        user = User.objects.create_user(username=data['username'], first_name=data['first_name'],
                                        last_name=data['last_name'], email=data['email'],
                                        password=data['password'])
        user.save()

        ud = UserDetails()
        ud.user = user

        if(data['mother'] != ''):
            ud.mother = User.objects.get(id=data['mother'])
        else:
            ud.mother = None

        if (data['father'] != ''):
            ud.mother = User.objects.get(id=data['father'])
        else:
            ud.father = None

        ud.is_doctor = data['is_doctor']
        ud.gender = data['gender']
        ud.date_of_birth = data['date_of_birth']
        ud.blood_group = data['blood_group']
        ud.address = data['address']
        ud.city = data['city']
        ud.iso_country_code = data['iso_country_code']
        ud.occupation = data['occupation']

        ud.save()

        return redirect('login')