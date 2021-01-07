from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect

from medical_visit.models import *
from usermgmt.models import UserDetails


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


    if (request.method == "GET"):
        visits = Visit.objects.filter(Q(doctor=request.user))

    elif (request.method == "POST"):
        data = request.POST


        if (data['category'] == 'patient_name'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    Q(patient__first_name__icontains=data['search_term']) | Q(
                        patient__last_name__icontains=data['search_term']) | Q(
                        patient__username__icontains=data['search_term'])))


        elif (data['category'] == 'purpose'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    purpose__icontains=data['search_term']))

        elif (data['category'] == 'diagnosis'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    diagnosis__icontains=data['search_term']))


        if(data['visit_date'] != ''):
            visits = visits.filter(date_time__date=data['visit_date'])


    ctxt['visits'] = visits.order_by('-date_time')

    return render(request, 'dashboard/doctor_dash/all_appointments.html', context=ctxt)


def medicalHistory(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'medical_history'

    patients = Visit.objects.filter(doctor=request.user).values('patient').distinct()
    patients_details = UserDetails.objects.filter(user__in=patients)


    if(request.method == "POST"):
        data = request.POST

        if(data['category'] == "patient_name"):
            patients_details = patients_details.filter(Q(user__first_name__icontains=data['search_term']) | Q(user__last_name__icontains=data['search_term']) | Q(user__username__icontains=data['search_term']))

        elif(data['category'] == "patient_id"):
            patients_details = patients_details.filter(user__id=data['search_term'])

        elif(data['category'] == "city"):
            patients_details = patients_details.filter(city__icontains=data['search_term'])


    ctxt['patients'] = patients_details

    return render(request, 'dashboard/doctor_dash/medical_history.html', context=ctxt)


def medicalProfile(request, patient_id):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'

    ctxt['patient_id'] = patient_id

    patient_details = UserDetails.objects.get(user__id=patient_id)
    ctxt['patient_details'] = patient_details
    doc_visits = Visit.objects.filter(Q(patient__id=patient_id) & Q(completed=True))

    if(request.method == 'POST'):
        data = request.POST

        if (data['category'] == 'doctor'):
            doc_visits = Visit.objects.filter(Q(patient__id=patient_id) & Q(completed=True) & Q(
                Q(doctor__username__icontains=data['search_term']) | Q(
                    doctor__first_name__icontains=data['search_term']) | Q(
                    doctor__last_name__icontains=data['search_term'])))
        elif (data['category'] == 'purpose'):
            doc_visits = Visit.objects.filter(
                Q(patient__id=patient_id) & Q(completed=True) & Q(purpose__icontains=data['search_term']))
        elif (data['category'] == 'diagnosis'):
            doc_visits = Visit.objects.filter(
                Q(patient__id=patient_id) & Q(completed=True) & Q(diagnosis__icontains=data['search_term']))

        elif(data['category'] == 'drug'):
            dv = DrugPrescription.objects.filter(Q(name__icontains=data['search_term']) & Q(visit__patient__id=patient_id)).values('visit').distinct()
            doc_visits = Visit.objects.filter(id__in=dv)

        elif (data['category'] == 'medical_test'):
            dv = TestPrescription.objects.filter(
                Q(name__icontains=data['search_term']) & Q(visit__patient__id=patient_id)).values('visit').distinct()
            doc_visits = Visit.objects.filter(id__in=dv)

        elif (data['category'] == 'vaccine'):
            dv = Vaccine.objects.filter(
                Q(name__icontains=data['search_term']) & Q(visit__patient__id=patient_id)).values('visit').distinct()
            doc_visits = Visit.objects.filter(id__in=dv)

    ctxt['visits'] = doc_visits

    return render(request, 'dashboard/doctor_dash/patient_profile.html', context=ctxt)



def appointmentFilling(request, visit_id):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['visit_id'] = visit_id
    visit = Visit.objects.get(id=visit_id)
    ctxt['visit'] = visit

    if(request.method == 'GET'):
        return render(request, 'dashboard/doctor_dash/appointment_filling.html', context=ctxt)

    elif(request.method == 'POST'):

        data = request.POST

        print('\n\nGot the form: \n'+str(data)+'\n\n')

        visit.diagnosis = data['diagnosis']
        visit.save()

        general_checkup = GeneralCheckup()
        general_checkup.visit = visit
        general_checkup.body_temperature_in_fahrenheit = data['body_temperature_in_fahrenheit']
        general_checkup.weight_in_kilograms = data['weight_in_kilograms']
        general_checkup.height_in_inches = data['height_in_inches']
        general_checkup.pulse_per_min = data['pulse_per_min']
        general_checkup.blood_pressure = data['blood_pressure']
        general_checkup.comments = data['comments']
        general_checkup.save()


        tongue_and_lip_examination = TongueAndLipExamination()
        tongue_and_lip_examination.visit = visit
        tongue_and_lip_examination.tongue_status = data['tongue_status']
        tongue_and_lip_examination.lip_status = data['lip_status']
        tongue_and_lip_examination.save()


        skin_examination = SkinExamination()
        skin_examination.visit = visit
        skin_examination.skin_type = data['skin_type']
        skin_examination.skin_pigment = data['skin_pigment']
        skin_examination.skin_color = data['skin_color']
        skin_examination.save()


        return redirect('prescription_filling', visit_id=visit_id)


def prescription_filling(request, visit_id):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['visit_id'] = visit_id

    ctxt['drug_prescriptions'] = DrugPrescription.objects.filter(visit__id=visit_id)
    ctxt['test_prescriptions'] = TestPrescription.objects.filter(visit_id=visit_id)
    ctxt['vaccines'] = Vaccine.objects.filter(visit_id=visit_id)

    if (request.method == 'GET'):
        return render(request, 'dashboard/doctor_dash/prescription_filling.html', context=ctxt)

    elif(request.method == 'POST'):
        data = request.POST

        visit = Visit.objects.get(id=visit_id)

        if(data['sub_type'] == 'drug_prescription'):
            dp = DrugPrescription()
            dp.visit = visit
            dp.name = data['name']
            dp.dosage = data['dosage']
            dp.frequency_per_day = data['frequency_per_day']
            dp.duration_in_days = data['duration_in_days']
            dp.comments = data['comments']
            dp.save()
            return redirect('prescription_filling', visit_id=visit_id)

        elif(data['sub_type'] == 'test_prescription'):
            tp = TestPrescription()
            tp.visit = visit
            tp.name = data['name']
            tp.save()
            return redirect('prescription_filling', visit_id=visit_id)

        elif(data['sub_type'] == 'vaccine'):
            vac = Vaccine()
            vac.visit = visit
            vac.name = data['name']
            vac.save()
            return redirect('prescription_filling', visit_id=visit_id)

        elif(data['sub_type'] == 'finish_visit'):
            visit.completed = True
            visit.save()
            return redirect('dd_mainDash')