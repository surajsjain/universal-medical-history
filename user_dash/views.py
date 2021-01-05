from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import render

from medical_visit.models import *
from usermgmt.models import UserDetails


# Create your views here.
def mainDash(request):
    ctxt = {}
    ctxt['dash_type'] = 'user'
    ctxt['active'] = 'dashboard'

    doc_visits = Visit.objects.filter(Q(patient=request.user) & Q(completed=False))
    ctxt['visits'] = doc_visits

    drug_prescriptions = DrugPrescription.objects.filter(visit__patient=request.user)
    current_prescriptions = []
    for drug in drug_prescriptions:
        time_limit = drug.visit.date_time + timedelta(days=drug.duration_in_days)
        if (datetime.now().date() <= time_limit.date()):
            current_prescriptions.append(drug)
    ctxt['drug_prescriptions'] = current_prescriptions

    test_prescriptions = TestPrescription.objects.filter(visit__patient=request.user)
    pending_tests = []
    for test in test_prescriptions:
        try:
            report = test.report
            url = report.url
        except:
            pending_tests.append(test)
    ctxt['test_prescriptions'] = pending_tests

    print(ctxt)

    return render(request, 'dashboard/user_dash/index.html', context=ctxt)


def prev_visits(request):
    ctxt = {}
    ctxt['dash_type'] = 'user'
    ctxt['active'] = 'prev_visits'

    if (request.method == "GET"):
        doc_visits = Visit.objects.filter(Q(patient=request.user) & Q(completed=True))

    elif (request.method == "POST"):
        data = request.POST
        if (data['category'] == 'doctor'):
            doc_visits = Visit.objects.filter(Q(patient=request.user) & Q(completed=True) & Q(
                Q(doctor__username__icontains=data['search_term']) | Q(
                    doctor__first_name__icontains=data['search_term']) | Q(
                    doctor__last_name__icontains=data['search_term'])))
        elif (data['category'] == 'purpose'):
            doc_visits = Visit.objects.filter(
                Q(patient=request.user) & Q(completed=True) & Q(purpose__icontains=data['search_term']))
        elif (data['category'] == 'diagnosis'):
            doc_visits = Visit.objects.filter(
                Q(patient=request.user) & Q(completed=True) & Q(diagnosis__icontains=data['search_term']))

    ctxt['visits'] = doc_visits

    return render(request, 'dashboard/user_dash/prev_visits.html', context=ctxt)


def doctor_search(request):
    ctxt = {}
    ctxt['dash_type'] = 'user'
    ctxt['active'] = 'doc_search'
    ctxt['same_city'] = True

    user_det = UserDetails.objects.get(user=request.user)
    user_city = user_det.city

    if(request.method == 'GET'):
        doctors = UserDetails.objects.filter(Q(city__icontains=user_city) & Q(is_doctor=True))


    elif(request.method == 'POST'):
        data = request.POST

        if(data['category'] == 'doctor'):
            doctors = UserDetails.objects.filter(Q(is_doctor=True) & Q(city__icontains=user_city) & Q(
                Q(user__username__icontains=data['search_term']) | Q(
                    user__first_name__icontains=data['search_term']) | Q(
                    user__last_name__icontains=data['search_term'])))

        elif(data['category'] == 'occupation'):
            doctors = UserDetails.objects.filter(Q(is_doctor=True) & Q(city__icontains=user_city) & Q(occupation__icontains=data['search_term']))

        elif(data['category'] == 'city'):
            ctxt['same_city'] = False
            ctxt['city'] = data['search_term']

            doctors = UserDetails.objects.filter(Q(is_doctor=True) & Q(city__icontains=data['search_term']))


    ctxt['doctors'] = doctors

    return render(request, 'dashboard/user_dash/doctor_search.html', context=ctxt)
