from django.contrib import admin
from .models import visitor,booked
# Register your models here.

class VisitorAdmin(admin.ModelAdmin):
    search_fields=['username']
    list_display=['username','email','city']

class BookedAdmin(admin.ModelAdmin):
    search_fields=['username']
    list_display=['username','hospital_name','hospital_city']

admin.site.register(visitor,VisitorAdmin)
admin.site.register(booked,BookedAdmin)
