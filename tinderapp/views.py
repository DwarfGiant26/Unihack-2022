from http.client import HTTPResponse
from ipaddress import ip_address
import re
from django.http import HttpResponse
from django.shortcuts import render
import tinderapp.auth as auth
import tinderapp.models as models
import tinderapp.discovery as discovery
from tinderapp.database import query,execute

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
    
    response = render(request,'before_discovery.html')
    response.set_cookie('email',email)
    discover_start(request,response,email)
    
    return response

def discovery_page(request):
    if request.COOKIES.get('num_of_discover') == 0:
        return HttpResponse("No one to discover")
    dic = discovered_info(request)
    return render(request,'discovery/discovery.html',dic)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if auth.check_password(email,password):
            response = render(request,'before_discovery.html')
            response.set_cookie('email',email)
            discover_start(request,response,email)
            return response
    
    # update location
    # ip = request.META.get("REMOTE_ADDR")
    # models.update_location(ip)

    return render(request,'login&register/index.html')

def style(request):
    return render(request,'login&register/style.css')

def discovered_info(request):
    likeStr = request.COOKIES.get('people_who_like')
    likeList = likeStr.split('-')
    discovered_index = get_discover_index(request)
    discovered_email = likeList[discovered_index]
    # get info about the person
    sql = f"""
        select username,interest,email
        from Users
        where email='{discovered_email}'
    """
    print(sql)
    name,interest,email = query(sql)[0]

    dic = {
        "name":name,
        "interests":interest.replace(',',', '),
        "email":email
    }
    
    return dic

def like(request):
    # Add to like list
    likeFrom = request.COOKIES.get('email')
    dic = discovered_info(request)
    response = render(request,'discovery/discovery.html',dic)
    update_discover_index(request,response)
    discovery.like(likeFrom, dic['email'])
    return response

def dislike(request):
    dic = discovered_info(request)
    response = render(request,'discovery/discovery.html',dic)
    update_discover_index(request,response)
    return response

def get_discover_index(request):
    index = request.COOKIES.get('discover_index')
    return int(index)

def update_discover_index(request,response):
    index = get_discover_index(request)
    # Increment like index
    new_discover_index = index + 1
    response.set_cookie('discover_index',new_discover_index)
    
    return index

def discover_start(request,response,email):
    response.set_cookie('discover_index',0)
    likeStr = '-'.join([elem[0] for elem in discovery.list_recommended_people(email)])
    response.set_cookie('num_of_discover',len(likeStr.split('-')))
    response.set_cookie('people_who_like',likeStr)

def discover_next(request):
    pass