from django.db import models
from matplotlib.pyplot import connect
import tinderapp.auth as auth
from tinderapp.database import create_connection


# Create your models here.


def register(username,email, password):
    auth.register(username,email,password)


