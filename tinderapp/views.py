from ipaddress import ip_address
import re
from django.shortcuts import render
import tinderapp.auth as auth
import tinderapp.models as models
import tinderapp.discovery as discovery

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

    return render(request,'discovery/discovery.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        if auth.check_password(email,password):
            response = render(request,'discovery/discovery.html')
            response.set_cookie('email',email)
            likeStr = discovery.list_recommended_people(email)
            response.set_cookie('people_who_like',likeStr)
            return response
    
    # update location
    # ip = request.META.get("REMOTE_ADDR")
    # models.update_location(ip)

    return render(request,'discovery/discovery.html')

def style(request):
    return render(request,'login&register/style.css')

def like(request):
    # Add to like list
    likeFrom = request.COOIES.get('email')
    likeStr = request.COOIES.get('people_who_like')
    likeList = list(likeStr.spilt(","))
    likeIndex = request.COOIES.get('like_index')
    response = render(request,'discovery/discovery.html')
    discovery.like(likeFrom, likeList[likeIndex])
    # Increment like index
    newLikeIndex = likeIndex + 1
    response.set_cookie('like_index',newLikeIndex)

    return response


