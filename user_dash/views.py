from datetime import datetime, timedelta
import os
from random import randint

from django.db.models import Q
from django.shortcuts import render, redirect

from medical_visit.models import *
from usermgmt.models import UserDetails
from data_offloader.filecoin import upload

from data_offloader.data_snapshot import snapshot_user_data
from data_offloader.ocean_script import publish_excel


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
        if(test.report_url == '' or test.report_url == None):
            pending_tests.append(test)

    ctxt['test_prescriptions'] = pending_tests

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


def book_visit(request, doctor_id):
    ctxt = {}
    ctxt['dash_type'] = 'user'

    if(request.method == "GET"):
        doctor = UserDetails.objects.get(user__id=doctor_id)
        ctxt['doctor'] = doctor

        return render(request, 'dashboard/user_dash/doctor_details.html', context=ctxt)

    elif(request.method == "POST"):
        data = request.POST

        doctor_visit = Visit()
        doctor_visit.patient = request.user
        doctor_visit.doctor = User.objects.get(id=data['doctor_id'])
        doctor_visit.date_time = data['date_time']
        doctor_visit.purpose = data['purpose']

        doctor_visit.save()

        return redirect('ud_mainDash')

def visit_details(request, visit_id, viewer):
    ctxt = {}
    if(viewer == 0):
        ctxt['dash_type'] = 'user'
    else:
        ctxt['dash_type'] = 'doctor'

    visit = Visit.objects.get(id=visit_id)
    ctxt['visit'] = visit
    patent_id = visit.patient.id
    doctor_id = visit.doctor.id

    ctxt['user_details'] = UserDetails.objects.get(user__id=patent_id)
    ctxt['doctor_details'] = UserDetails.objects.get(user__id=doctor_id)

    try:
        ctxt['general_checkup'] = GeneralCheckup.objects.get(visit__id=visit_id)
    except:
        ctxt['general_checkup'] = None

    try:
        ctxt['skin_examination'] = SkinExamination.objects.get(visit__id=visit_id)
    except:
        ctxt['skin_examination'] = None

    try:
        ctxt['tongue_and_lip_examination'] = TongueAndLipExamination.objects.get(visit__id=visit_id)
    except:
        ctxt['tongue_and_lip_examination'] = None

    # Will return an array
    ctxt['vaccinations'] = Vaccine.objects.filter(visit__id=visit_id)
    ctxt['drug_prescriptions'] = DrugPrescription.objects.filter(visit__id=visit_id)
    ctxt['test_prescriptions'] = TestPrescription.objects.filter(visit__id=visit_id)

    return render(request, 'dashboard/common_pages/visit_details.html', context=ctxt)


def test_prescription_report_upload(request, test_prescription_id):
    ctxt = {}
    ctxt['dash_type'] = 'user'

    if(request.method == 'GET'):

        ctxt['test_prescription_id'] = test_prescription_id

        return render(request, 'dashboard/user_dash/report_upload.html', context=ctxt)

    elif(request.method == 'POST'):
        data = request.POST
        medical_test = TestPrescription.objects.get(id=data['test_id'])
        report_file = request.FILES['report']

        new_file_name = 'test_' + str(test_prescription_id) + '_report.pdf'
        report_file.name = new_file_name

        uploaded_report_url = upload(report_file)
        medical_test.report_url = uploaded_report_url



        medical_test.save()

        return redirect('ud_mainDash')


def sell_data(request):
    ctxt = {}
    ctxt['dash_type'] = 'user'
    ctxt['published'] = False

    if(request.method == 'POST'):
        data = request.POST

        url = snapshot_user_data(request.user, data['month'], data['year'])

        dt_name = "User" + str(request.user.id) + "_" + str(data["month"]) + "_" + str(data['year'])
        dt_symbol = "UMH-" + str(request.user.id) + "-" + str(data["month"]) + "-" + str(data['year']) + '-' + str(randint(0, 100))
        dataset_name = request.user.first_name + ' ' + request.user.last_name + "'s medical histroy from " + str(data["month"]) + "/" + str(data['year'])

        did = publish_excel(data['private_key'], url, dt_name, dt_symbol, dataset_name, request.user.username)

        ctxt['did'] = did
        ctxt['dt_symbol'] = dt_symbol
        ctxt['published'] = True


    return render(request, 'dashboard/user_dash/sell_data.html', context=ctxt)