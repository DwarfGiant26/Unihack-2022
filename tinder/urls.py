"""tinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tinderapp.discovery import like
import tinderapp.views as views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register),
    path('',views.login),
    path('style',views.style),
    path('signup',csrf_exempt(views.signup)),
    path('login',csrf_exempt(views.login)),
    path('submit_profile',csrf_exempt(views.submit_profile)),
    path('like', csrf_exempt(views.like)),
    path('dislike',csrf_exempt(views.dislike)),
    path('discovery',views.discovery_page),
    path('profile',views.profile),
    path('profile_settings',views.profile_settings),
    path('chat',views.chat),
    path('stats',views.stats),
]
