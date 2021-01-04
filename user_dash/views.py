from django.shortcuts import render

# Create your views here.
def mainDash(request):
    return render(request, 'dashboard/user_dash/index.html')