from django.contrib import admin
from shops.models import Shop
from employee.models import Employee
from employee_experience.models import Employee_Experience
from employee_availability.models import Employee_Availability
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Shop,Employee,Employee_Experience,Employee_Availability)

class ViewAdmin(ImportExportModelAdmin):
    pass
