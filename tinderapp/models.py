from django.db import models
from matplotlib.pyplot import connect
import tinderapp.auth as auth
from tinderapp.database import create_connection,execute,query
# from django.contrib.gis.geoip2 import GeoIP2

# Create your models here.
def update_location(email,ip):
    g = GeoIP2()
    latitude,longitude = g.lat_lon(ip)

    #update sql
    sql = f"""
        update Users
        set latitude = {latitude}, 
            longitude = {longitude}
        where email = '{email}';
    """
    execute(sql)

def update_profile(request,email,birthday,postcode,travel_dist,interest,min_age,max_age,description,name):
    #update sql
    sql = f"""
        update Users
        set username = '{name}',
            birthday = '{birthday}', 
            postcode = '{postcode}',
            max_radius = {travel_dist},
            min_age = {min_age},
            max_age = {max_age},
            interest = '{interest}',
            description = '{description}',
            email = '{email}'
        where email = '{request.COOKIES.get('email')}';
    """
    print(sql)
    execute(sql)

