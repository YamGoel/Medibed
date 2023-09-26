from django.contrib import admin
from .models import hospital,bedsubmit
# Register your models here.

class HospitalAdmin(admin.ModelAdmin):
    search_fields=['hospital_name']
    list_display=['hospital_username','hospital_name','hospital_city']
admin.site.register(hospital,HospitalAdmin)

class BedAdmin(admin.ModelAdmin):
    search_fields=['hospital_name']
    list_display=['hospital_name','hospital_city','beds','occupied','available','price']
admin.site.register(bedsubmit,BedAdmin)
