from ipaddress import ip_address
from django.shortcuts import render
import tinderapp.auth as auth
import tinderapp.models as models

# Create your views here.
def register(request):
    return render(request,'login&register/index.html')

def signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    auth.register(username,email,password)
    dic = {
        "name": username,
        "email": email,
        "password": password,
    }
    return profile_settings(request,dic)

def profile_settings(request,dic=None):
    return render(request,'ProfileSettings/ProfileSettings.html',dic)

def submit_profile(request):
    email = request.POST.get('email')
    birthday = request.POST.get('birthday')
    postcode = request.POST.get('postcode')
    travel_dist = request.POST.get('travel_dist')
    interest = ','.join(request.POST.getlist('interest'))
    min_age = request.POST.get('min_age')
    max_age = request.POST.get('max_age')
    models.update_profile(email,birthday,postcode,travel_dist,interest,min_age,max_age)

    return discovery(request)

def discovery(request):
    return render(request,'discovery/discovery.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        if auth.check_password(email,password):
            response = render(request,'discovery/discovery.html')
            response.set_cookie('email',email)
            return response
    
    # update location
    # ip = request.META.get("REMOTE_ADDR")
    # models.update_location(ip)

    return render(request,'login&register/index.html')

def style(request):
    return render(request,'login&register/style.css')
