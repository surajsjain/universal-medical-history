from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from medical_visit.models import *


# Create your views here.
def todayAppointments(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'today_appointments'

    if (request.method == "GET"):
        visits = Visit.objects.filter(
            Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False))

    elif (request.method == "POST"):
        data = request.POST

        if (data['category'] == 'patient_name'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False) & Q(
                    Q(patient__first_name__icontains=data['search_term']) | Q(
                        patient__last_name__icontains=data['search_term']) | Q(
                        patient__username__icontains=data['search_term'])))


        elif (data['category'] == 'purpose'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False) & Q(
                    purpose__icontains=data['search_term']))



    ctxt['visits'] = visits.order_by('date_time')

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
