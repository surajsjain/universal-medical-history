from .utils import queryset_to_excel
from django.db.models import Q

from medical_visit.models import *
from usermgmt.models import UserDetails

import os
from .filecoin import upload

def snapshot_user_data(user, month, year):
    q_dict={}
    deferred = {}

    q_dict['basic_details'] = UserDetails.objects.defer('address').filter(user=user)
    deferred['basic_details'] = ['address']

    q_dict['visits'] = Visit.objects.filter(Q(patient=user) & Q(date_time__month=month) & Q(date_time__year=year))
    q_dict['general_checkups'] = GeneralCheckup.objects.filter(visit__in=q_dict['visits'])
    q_dict['tongue_and_lip_examinations'] = TongueAndLipExamination.objects.filter(visit__in=q_dict['visits'])
    q_dict['skin_examinations'] = SkinExamination.objects.filter(visit__in=q_dict['visits'])
    q_dict['vaccines'] = Vaccine.objects.filter(visit__in=q_dict['visits'])
    q_dict['drug_prescriptions'] = DrugPrescription.objects.filter(visit__in=q_dict['visits'])
    q_dict['medical_tests'] = TestPrescription.objects.filter(visit__in=q_dict['visits'])

    file_path = 'media/' + user.username + '_' + str(month) + '_' + str(year) + '.xls'

    queryset_to_excel(q_dict, file_path, deferred)

    url = upload(open(file_path, 'rb'))

    os.remove(file_path)

    return url