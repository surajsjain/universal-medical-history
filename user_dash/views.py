from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Q

from medical_visit.models import *

# Create your views here.
def mainDash(request):
    ctxt = {}

    doc_visits = Visit.objects.filter(Q(patient=request.user) & Q(completed = False))
    ctxt['visits'] = doc_visits

    drug_prescriptions = DrugPrescription.objects.filter(visit__patient = request.user)
    current_prescriptions = []
    for drug in drug_prescriptions:
        time_limit = drug.visit.date_time + timedelta(days= drug.duration_in_days)
        if(datetime.now().date() <= time_limit.date()):
            current_prescriptions.append(drug)
    ctxt['drug_prescriptions'] = current_prescriptions


    test_prescriptions = TestPrescription.objects.filter(visit__patient = request.user)
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