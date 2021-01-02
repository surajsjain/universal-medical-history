from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mother = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="parent_mother")
    father = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="parent_father")

    is_doctor = models.BooleanField(default=False)

    gender = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(default=now)
    blood_group = models.CharField(max_length=5, blank=True)

    address = models.CharField(max_length=300)
    city = models.CharField(max_length=20)
    iso_country_code = models.CharField(max_length=5)

    occupation = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return str(self.user.id) + " - " + str(self.user.username)
