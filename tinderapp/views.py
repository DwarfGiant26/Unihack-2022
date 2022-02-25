from django.shortcuts import render
import tinderapp.models

# Create your views here.
def register(request):
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # models.register(username,password)
    render(request,'tinderapp/templates/login&register/index.html')

def login(request):
    render(request,'login&register/index.html')
