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
    if dic == None:
        sql=f"""
            select username,email,password,birthday,postcode,max_radius,interest,min_age,max_age,description
            from Users
            where email='{request.COOKIES.get('email')}'
        """
        name,email,password,birthday,postcode,max_radius,interest,min_age,max_age,description = query(sql)[0]
        dic = {
            "name":name,
            "email":email,
            "password":password,
            "birthday":birthday,
            "postcode":postcode,
            "max_dist":max_radius,
            "min_age":min_age,
            "max_age":max_age,
            "description":description,
        }
    return render(request,'ProfileSettings-Arif/profile-settings.html',dic)

def profile(request):
    sql=f"""
        select username,interest,cast(strftime('%Y', 'now') - strftime('%Y', birthday) as int) as age
        from Users
        where email='{request.COOKIES.get("email")}'
    """
    name,interest,age = query(sql)[0]
    dic={
        "name":name,
        "interest":interest,
        "age":age
    }
    return render(request,'profile.html',dic)

def stats(request):
    dic = {}
    return render(request,'stats/stats1.html',dic)

def chat(request):
    dic = {}
    return render(request,'messages/message2.html',dic)

def submit_profile(request):
    email = request.POST.get('email')
    birthday = request.POST.get('birthday')
    postcode = request.POST.get('postcode')
    travel_dist = request.POST.get('max_dist')
    interest = ','.join(request.POST.getlist('interest'))
    min_age = request.POST.get('min_age')
    max_age = request.POST.get('max_age')
    description = request.POST.get('description')
    name = request.POST.get('name')
    models.update_profile(request,email,birthday,postcode,travel_dist,interest,min_age,max_age,description,name)
    
    response = render(request,'before_discovery.html')
    response.set_cookie('email',email)
    discover_start(request,response,email)
    
    return response

def discovery_page(request):
    if get_discover_index(request) >= int(request.COOKIES.get('num_of_discover')):
        return HttpResponse("No one to discover")
    dic = discovered_info(request)
    response = render(request,'discovery/discovery.html',dic)
    update_discover_index(request,response)
    return response

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
    discovered_index = get_discover_index(request) % int(request.COOKIES.get('num_of_discover'))
    discovered_email = likeList[discovered_index]
    # get info about the person
    sql = f"""
        select username,interest,email,cast(strftime('%Y', 'now') - strftime('%Y', birthday) as int) as age,description
        from Users
        where email='{discovered_email}'
    """
    print(sql)
    name,interest,email,age,description = query(sql)[0]

    dic = {
        "name":name,
        "interests":interest.replace(',',', '),
        "email":email,
        "age":age,
        "description":description
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
    recommended = discovery.list_recommended_people(email)
    likeStr = '-'.join([elem[0] for elem in recommended])
    response.set_cookie('num_of_discover',len(recommended))
    response.set_cookie('people_who_like',likeStr)

def discover_next(request):
    pass