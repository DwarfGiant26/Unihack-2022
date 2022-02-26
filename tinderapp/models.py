from django.db import models
from matplotlib.pyplot import connect
import tinderapp.auth as auth
from tinderapp.database import create_connection,execute,query
from django.contrib.gis.geoip2 import GeoIP

# Create your models here.
def update_location(email,ip):
    g = GeoIP()
    latitude,longitude = g.lat_lon(ip)

    #update sql
    sql = f"""
        update Users
        set latitude = {latitude}, 
            longitude = {longitude}
        where email = '{email}';
    """
    execute(sql)

def update_profile(email,description,picture,max_radius,interest):
    #update sql
    sql = f"""
        update Users
        set description = {description}, 
            max_radius = {max_radius},
            interest = '{interest}'
        where email = '{email}';
    """
    execute(sql)

