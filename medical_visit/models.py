from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Visit(models.Model):
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor')
    date_time = models.DateTimeField(default=now)
    completed = models.BooleanField(default=False)
    purpose = models.CharField(max_length=3000, default='')

    diagnosis = models.CharField(max_length=3000, default='', blank=True)

class GeneralCheckup(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    body_temperature_in_fahrenheit = models.FloatField(blank=True)
    weight_in_kilograms = models.FloatField(blank=True)
    height_in_inches = models.FloatField(blank=True)

    pulse_per_min = models.IntegerField(blank=True, null=True, default=None)
    blood_pressure = models.IntegerField(blank=True, null=True, default=None)

class Vaccine(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)

class DrugPrescription(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)

    frequency_per_day = models.IntegerField()
    duration_in_days = models.IntegerField()

    comments = models.CharField(max_length=2000)