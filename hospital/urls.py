from django.urls import path,re_path
from . import views

urlpatterns = [
    path("hospitalsignup",views.hospitalsignup,name='hospitalsignup'),
    path("hospitalsignin",views.hospitalsignin,name="hospitalsignin"),
    path("hospitalhome",views.hospitalhome,name="hospitalhome"),
    path("hospitaloccupied",views.hospitaloccupied,name="hospitaloccupied"),
    path("submitbed",views.submitbed,name="submitbed"),
    path("submitprice",views.submitprice,name="submitprice"),
    path("delete",views.delete,name="delete"),
    path("freeup",views.freeup,name="freeup"),
    path("h_logout",views.h_logout,name="h_logout"),
]
