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
    return render(request,'login&register/index.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    

def login(request):
    return render(request,'login&register/index.html')

def style(request):
    print("sdfasdfasdfasdfasdf")
    return render(request,'login&register/style.css')
