from django.shortcuts import render

# Create your views here.
def mainDash(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'

    return render(request, 'dashboard/doctor_dash/index.html', context=ctxt)