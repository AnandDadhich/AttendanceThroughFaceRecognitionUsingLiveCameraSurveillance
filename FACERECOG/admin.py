from django.contrib import admin
from .models import EmployeeInfo, AboutEmployees, ContactUs
from django.utils import timezone

# Register your models here.
@admin.register(EmployeeInfo)
class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display = ('name','id','date_created','days_since_creation')
    search_fields=('name',)
    fields=(('id','name'),)
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)

    def days_since_creation(self,emp):
        diff=timezone.now() - emp.date_created
        return diff.days
    days_since_creation.short_description = "Active days"

admin.site.register(AboutEmployees)
admin.site.register(ContactUs)

#admin.site.register(EmployeeInfo)

