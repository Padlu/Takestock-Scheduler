from django.db import models

# Create your models here.
#id	first_name	initials	is_supervisor	pay_rate	has_car

class Employee(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15, blank=False)
    initials = models.CharField(max_length=5, blank=False)
    is_supervisor = models.BooleanField(default=True)
    pay_rate = models.IntegerField(default=None)
    has_car = models.BooleanField(default=True)

