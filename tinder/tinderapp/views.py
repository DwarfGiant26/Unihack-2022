from django.shortcuts import render
import models

# Create your views here.
def register(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    models.register(username,password)