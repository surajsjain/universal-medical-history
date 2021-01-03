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