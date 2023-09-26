from django.urls import path,re_path
from . import views

urlpatterns = [
    path("visitorsignup",views.visitorsignup,name='visitorsignup'),
    path("visitorsignin",views.visitorsignin,name="visitorsignin"),
    path("visitorhome",views.visitorhome,name="visitorhome"),
    path("booking",views.booking,name="booking"),
    path("cancel",views.cancel,name="cancel"),
    path("booking_details",views.booking_details,name="booking_details"),
    path("logout",views.logout,name="logout"),
]
