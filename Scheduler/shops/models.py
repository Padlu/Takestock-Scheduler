from django.db import models

# Create your models here.
# shop_id	brand	initials	name	has_deli	deli_size	has_stockroom	stockroom_size	no_of_people_in_stockroom	has_off_licence	off_licence_size	no_of_people_in_offlicence	behind_till_size	toiletries_size	shop_size	stock_size_price_range	avg_min_crew_size

class Shop(models.Model):

    # choices for data integrity/normality
    size_choices = (
        ('Big', 'Department/Store size is Big'),
        ('Mid', 'Department/Store size is Medium'),
        ('Small', 'Department/Store size is Small'),
        ('No', "We don't do that department")
    )

    # brand choices
    brand_choices = (
        ('SuperValu', 'SuperValu'),
        ('Centra', 'Centra'),
        ('Spar', 'Spar')
    )

    # brand_initials choices
    brand_initials_choices = (
        ('SV', 'SuperValu'),
        ('CTA', 'Centra'),
        ('SPAR', 'Spar')
    )

    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=15, choices=brand_choices, blank=False)
    initials = models.CharField(max_length=5, choices=brand_initials_choices, blank=False)
    name = models.CharField(max_length=5, blank=False)
    has_deli = models.BooleanField(default=True)
    deli_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    has_stockroom = models.BooleanField(default=True)
    stockroom_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    no_of_people_in_stockroom = models.IntegerField()
    has_off_licence = models.BooleanField(default=True)
    off_licence_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    no_of_people_in_offlicence = models.IntegerField()
    behind_till_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    toiletries_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    shop_size = models.CharField(max_length=5, choices=size_choices, blank=False)
    stock_size_price_range = models.IntegerField(default=None)
    avg_min_crew_size = models.IntegerField(default=None)

