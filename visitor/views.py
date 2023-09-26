from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password , check_password
from .models import visitor,booked
from hospital import views
from base import views
from hospital.models import hospital,bedsubmit
# Create your views here.

vis_name = ''
vis_city=''

def cancel(request):
    if booked.objects.filter(username=vis_name).exists():
        c = booked.objects.get(username=vis_name)
        y = bedsubmit.objects.get(hospital_name=c.hospital_name,hospital_city=vis_city)
        y.occupied= int(y.occupied)-1
        y.available= int(y.available)+1
        y.save()
        c.delete()
        return redirect('visitorhome')
    else:
        messages.info(request,'You dont have any booking to cancel.')
        return redirect('visitorhome')

def booking(request):
    if request.method == 'POST':
        n = request.POST.get('name')
        ob = bedsubmit.objects.get(hospital_name=n,hospital_city=vis_city)
        av = int(ob.available)
        if av==0:
            messages.info(request,'No beds available in this hospital.')
            return redirect('visitorhome')
        else:
            if booked.objects.filter(username=vis_name).exists():
                messages.info(request,'You already have 1 booking.')
                return redirect('visitorhome')
            else:
                # n = request.POST.get('name')
                # print(n)
                vis = visitor.objects.get(username=vis_name)
                vis_email_id = vis.email
                hos = hospital.objects.get(hospital_name=n,hospital_city=vis_city)
                hos_email_id = hos.hospital_email
                books = booked(username=vis_name,vis_email=vis_email_id,hospital_name=n,hospital_city=vis_city,hospital_email=hos_email_id)
                books.save()
                x = bedsubmit.objects.get(hospital_name=n,hospital_city=vis_city)
                x.occupied= int(x.occupied)+1
                x.available= int(x.available)-1
                x.save()
                return redirect('visitorhome')

def visitorhome(request):
    if request.session.has_key('visitor_username'):
        hos = bedsubmit.objects.filter(hospital_city=vis_city ).values_list('hospital_name','beds','occupied','available','price')
        d = { 'name':request.session["visitor_username"],'city':vis_city ,'hos':hos}
        # print('You are:',request.session.get('visitor_username'))
        return render(request,'visitor_home/homepage.html',d)
    else:
        messages.info(request,'Login first/again')
        return redirect('visitorsignin')

def visitorsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        city = request.POST.get('city').lower()
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password)<8:
            messages.info(request,'Password must of minimum 8 Characters.')
            return redirect('visitorsignup')
        else:
            if password == password2:
                if visitor.objects.filter(username=username).exists():
                    messages.info(request,'Hospital name already in use.')
                    return redirect('visitorsignup')
                elif visitor.objects.filter(email=email).exists():
                    messages.info(request,'Email already in use.')
                    return redirect('visitorsignup')
                else:
                    password = make_password(password)
                    user = visitor(username=username,email=email,city=city,password=password)
                    user.save()
                    return redirect('visitorsignin')
            else:
                messages.info(request,'Password and Confirm Password not Matching')
                return redirect('visitorsignup')
        return redirect('/')
    else:
        return render(request,'visitor/signup.html')

def visitorsignin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if visitor.objects.filter(username=username).exists():
            obje = visitor.objects.get(username=username)
            f = check_password(password,obje.password)
            if f:
                global vis_name
                vis_name = obje.username
                global vis_city
                vis_city = obje.city
                request.session['visitor_username'] = username
                request.session.set_expiry(0)
                return redirect("visitorhome")
            else:
                messages.info(request,'Wrong credentials')
                return redirect('visitorsignin')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('visitorsignin')
    else:
        return render(request,'visitor/signin.html')


def booking_details(request):
    if request.session.has_key('visitor_username'):
        if booked.objects.filter(username=vis_name).exists():
            # book_details = booked.objects.get(username=vis_name)
            b = booked.objects.filter(username=vis_name).values_list('hospital_name','hospital_email')
            obj1 = booked.objects.get(username=vis_name)
            hos_name = obj1.hospital_name
            hos_city = obj1.hospital_city
            obj2 = hospital.objects.get(hospital_name=hos_name,hospital_city=hos_city)
            add = obj2.address
            d = { 'book_details':b,'add':add}
            return render(request,'visitor_home/bookings.html',d)
        else:
            messages.info(request,'You dont have any booking.')
            return redirect("visitorhome")
    else:
        messages.info(request,'Login first/again')
        return redirect('visitorsignin')

def logout(request):
    if request.session.has_key('visitor_username'):
        del request.session['visitor_username']
        return redirect("index")
    else:
        messages.info(request,'Login first/again')
        return redirect('visitorsignin')
