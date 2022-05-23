from django.db import models

# Create your models here.
# id	initials	available 1	available 2	available 3	available 4	available 5	available 6	available 7	available 8	available 9	available 10	available 11	available 12	available 13	available 14	available 15	available 16	available 17	available 18	available 19	available 20	available 21	available 22	available 23	available 24	available 25	available 26	available 27	available 28	available 29	available 30	available 31

class Employee_Availability(models.Model):

    id = models.AutoField(primary_key=True)
    initials = models.CharField(max_length=5, blank=False)
    available_1 = models.IntegerField(default=0)
    available_2 = models.IntegerField(default=0)
    available_3 = models.IntegerField(default=0)
    available_4 = models.IntegerField(default=0)
    available_5 = models.IntegerField(default=0)
    available_6 = models.IntegerField(default=0)
    available_7 = models.IntegerField(default=0)
    available_8 = models.IntegerField(default=0)
    available_9 = models.IntegerField(default=0)
    available_10 = models.IntegerField(default=0)
    available_11 = models.IntegerField(default=0)
    available_12 = models.IntegerField(default=0)
    available_13 = models.IntegerField(default=0)
    available_14 = models.IntegerField(default=0)
    available_15 = models.IntegerField(default=0)
    available_16 = models.IntegerField(default=0)
    available_17 = models.IntegerField(default=0)
    available_18 = models.IntegerField(default=0)
    available_19 = models.IntegerField(default=0)
    available_20 = models.IntegerField(default=0)
    available_21 = models.IntegerField(default=0)
    available_22 = models.IntegerField(default=0)
    available_23 = models.IntegerField(default=0)
    available_24 = models.IntegerField(default=0)
    available_25 = models.IntegerField(default=0)
    available_26 = models.IntegerField(default=0)
    available_27 = models.IntegerField(default=0)
    available_28 = models.IntegerField(default=0)
    available_29 = models.IntegerField(default=0)
    available_30 = models.IntegerField(default=0)
    available_31 = models.IntegerField(default=0)

