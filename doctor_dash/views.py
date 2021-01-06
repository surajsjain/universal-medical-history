from django.shortcuts import render

# Create your views here.
def todayAppointments(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'today_appointments'

    return render(request, 'dashboard/doctor_dash/today_appointments.html', context=ctxt)


def allAppointments(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'all_appointments'

    return render(request, 'dashboard/doctor_dash/all_appointments.html', context=ctxt)


def medicalHistory(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'medical_history'

    return render(request, 'dashboard/doctor_dash/medical_history.html', context=ctxt)