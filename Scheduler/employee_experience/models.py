from django.db import models

# Create your models here.
# emp_id	initials	no_of_jobs_worked	no_years_at_takestock	approx_no_of_jobs_done	exp_level	no_of_ctas_worked	no_of_svs_worked	no_of_sprs_worked	do_deli	deli_count	do_off_licence	off_licence_count	do_behind_till	behind_till_count	do_stockroom	stockroom_count	do_toiletries	toiletries_count

class Employee_Experience(models.Model):

    # choices for data integrity/normality
    exp_level_choices = (
        ('Expert', 'Expert'),
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Mid', "Mid"),
        ('Low', 'Low')
    )

    id = models.AutoField(primary_key=True)
    initials = models.CharField(max_length=5, blank=False)
    no_of_jobs_worked = models.IntegerField(default=None)
    no_years_at_takestock = models.IntegerField(default=None)
    approx_no_of_jobs_done = models.IntegerField(default=None)
    exp_level = models.CharField(max_length=15, choices=exp_level_choices, blank=False)
    no_of_ctas_worked = models.IntegerField(default=None)
    no_of_svs_worked = models.IntegerField(default=None)
    no_of_sprs_worked = models.IntegerField(default=None)
    do_deli = models.BooleanField(default=True)
    deli_count = models.IntegerField(default=None)
    do_off_licence = models.BooleanField(default=True)
    off_licence_count = models.IntegerField(default=None)
    do_behind_till = models.BooleanField(default=True)
    behind_till_count = models.IntegerField(default=None)
    do_stockroom = models.BooleanField(default=True)
    stockroom_count = models.IntegerField(default=None)
    do_toiletries = models.BooleanField(default=True)
    toiletries_count = models.IntegerField(default=None)

