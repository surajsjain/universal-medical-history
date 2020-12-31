from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    gender = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(default= datetime.now())
    blood_group = models.CharField(max_length=5, blank=True)

    address = models.CharField(max_length=300)
    city = models.CharField(max_length=20)
    iso_country_code = models.CharField(max_length=5)

    occupation = models.CharField(max_length=40, blank=True)
