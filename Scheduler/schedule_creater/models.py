from django.db import models

# Create your models here.

# class Employee_Inherited(models.Model):
#
#     id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=15, blank=False)
#     initials = models.CharField(max_length=5, blank=False)
#     is_supervisor = models.BooleanField(default=True)
#     pay_rate = models.IntegerField(default=None)
#     has_car = models.BooleanField(default=True)
#
# class Shop_Inherited(models.Model):
#
#     id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=15, blank=False)
#     initials = models.CharField(max_length=5, blank=False)
#     is_supervisor = models.BooleanField(default=True)
#     pay_rate = models.IntegerField(default=None)
#     has_car = models.BooleanField(default=True)