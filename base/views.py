from django.shortcuts import render,redirect
from django.contrib import messages
import smtplib
from .models import feedback

# Create your views here.
def index(request):
    return render(request,'index.html')

def feedback_page(request):
    if request.method=='POST':
        full_name = request.POST.get('feedusername')
        email = request.POST.get('feedemail')
        feed = request.POST.get('feedback')
        feedback_s = feedback(full_name=full_name,email=email,feed=feed)
        feedback_s.save();
        messages.success(request,'Feedback Submitted!')
        return redirect('/feedback_page')
    return render(request,'feedback.html')

def aboutus(request):
    data = feedback.objects.values('full_name','feed')
    return render(request,'aboutus.html',{'data':data})
