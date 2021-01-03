from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Visit)
admin.site.register(GeneralCheckup)
admin.site.register(TongueAndLipExamination)
admin.site.register(SkinExamination)
admin.site.register(Vaccine)
admin.site.register(DrugPrescription)
admin.site.register(TestPrescription)
