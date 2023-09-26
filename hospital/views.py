from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password , check_password
from .models import hospital,bedsubmit
from base import views
from visitor.models import booked,visitor
# Create your views here.

name=''
city=''

def hospitalsignup(request):
    if request.method == 'POST':
        hospital_username = request.POST.get('hospitalusername')
        hospital_name = request.POST.get('hospitalname')
        hospital_email = request.POST.get('hospitalemail')
        hospital_city = request.POST.get('hospitalcity').lower()
        address = request.POST.get('hospitaladdress')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(password)<8:
            messages.info(request,'Password must of minimum 8 Characters.')
            return redirect('hospitalsignup')
        else:
            if password==password2:
                if hospital.objects.filter(hospital_username=hospital_username).exists():
                    messages.info(request,'Hospital is already registered in the given address.')
                    return redirect('hospitalsignup')
                elif hospital.objects.filter(hospital_email=hospital_email).exists():
                    messages.info(request,'Email already in use.')
                    return redirect('hospitalsignup')
                elif hospital.objects.filter(hospital_name=hospital_name,hospital_city=hospital_city).exists():
                    messages.info(request,'Hospital name in this city is already registered.')
                    return redirect('hospitalsignup')
                else:
                    password = make_password(password)
                    user = hospital(hospital_username=hospital_username,hospital_name=hospital_name,hospital_city=hospital_city,hospital_email=hospital_email,address=address,password=password,)
                    user.save();
                    return redirect('hospitalsignin')
            else:
                messages.info(request,'Password and Confirm Password not Matching')
                return redirect('hospitalsignup')
        return redirect('/')
    else:
        return render(request,'hospital/signup.html')

def hospitalsignin(request):
    if request.method == 'POST':
        hospital_username = request.POST.get('hospitalusername')
        password = request.POST.get('password')
        if hospital.objects.filter(hospital_username=hospital_username).exists():
            obj = hospital.objects.get(hospital_username=hospital_username)
            flag = check_password(password,obj.password)
            if flag:
                global name
                name = obj.hospital_name
                global city
                city = obj.hospital_city
                request.session['hospital_username'] = hospital_username
                request.session.set_expiry(0)
                return redirect("hospitalhome")
            else:
                messages.info(request,'Wrong credentials')
                return redirect('hospitalsignin')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('hospitalsignin')
    else:
        return render(request,'hospital/signin.html')

def hospitalhome(request):
    if request.session.has_key('hospital_username'):
        if bedsubmit.objects.filter(hospital_name=name,hospital_city=city).exists():
            show = bedsubmit.objects.get(hospital_name=name)
            no_bed=show.beds
            price_bed=show.price
            beds_occupied=show.occupied
            beds_avail=show.available
            d = { 'name':name,'no_bed':no_bed,'price_bed':price_bed,'beds_occupied':beds_occupied,'beds_avail':beds_avail}
            return render(request,"hospital_home/homepage.html",d)
        else:
            no_bed=''
            price_bed=''
            beds_avail=''
            d = { 'name':name,'no_bed':no_bed,'price_bed':price_bed,'beds_avail':beds_avail}
            return render(request,"hospital_home/homepage.html",d)
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')


def hospitaloccupied(request):
    if request.session.has_key('hospital_username'):
        b = booked.objects.filter(hospital_name=name,hospital_city=city).values_list('username','vis_email')
        d = { 'username':b}
        return render(request,"hospital_home/occupied.html",d)
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')

def freeup(request):
    if request.method == 'POST':
        n = request.POST.get('name')
        f = booked.objects.get(username=n)
        f.delete()
        y = bedsubmit.objects.get(hospital_name=name,hospital_city=city)
        y.occupied= int(y.occupied)-1
        y.available= int(y.available)+1
        y.save()
        return redirect('hospitaloccupied')

def submitbed(request):
    if request.session.has_key('hospital_username'):
        if request.method == 'POST':
            beds = request.POST.get('beds')
            if bedsubmit.objects.filter(hospital_name=name,hospital_city=city).exists():
                o = bedsubmit.objects.get(hospital_name=name)
                prices = o.price
                o.beds= int(o.beds)+int(beds)
                o.available=int(o.beds) - int(o.occupied)
                o.save()
                return redirect('hospitalhome')
            else:
                messages.info(request,'Set a price for your bed first to add beds.')
                return redirect('hospitalhome')
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')

def submitprice(request):
    if request.session.has_key('hospital_username'):
        if request.method == 'POST':
            price = request.POST.get('price')
            if bedsubmit.objects.filter(hospital_name=name,hospital_city=city).exists():
                p = bedsubmit.objects.get(hospital_name=name)
                p.available=int(p.beds)-int(p.occupied)
                p.price=price
                p.save()
                return redirect('hospitalhome')
            else:
                priceset = bedsubmit(hospital_name=name,hospital_city=city,available=0,beds=0,occupied='0',price=price)
                priceset.save();
                return redirect('hospitalhome')
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')

def delete(request):
    if request.session.has_key('hospital_username'):
        if request.method == 'POST':
            delete = request.POST.get('delete')
            if bedsubmit.objects.filter(hospital_name=name,hospital_city=city).exists():
                d = bedsubmit.objects.get(hospital_name=name)
                if int(delete) > int(d.available):
                    messages.info(request,'Wrong number of beds.')
                    return redirect('hospitalhome')
                else:
                    d.beds=int(d.beds)-int(delete)
                    d.available=int(d.beds)-int(d.occupied)
                    d.save()
                    return redirect('hospitalhome')
            else:
                messages.info(request,'Register beds and set price.')
                return redirect('hospitalhome')
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')


def h_logout(request):
    if request.session.has_key('hospital_username'):
        del request.session['hospital_username']
        return redirect("index")
    else:
        messages.info(request,'Login first/again')
        return redirect('hospitalsignin')
