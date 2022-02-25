from django.db import models
from matplotlib.pyplot import connect
from tinderapp.auth import register
from tinderapp.database import create_connection

db_file = "../db.sqlite3"
# Create your models here.

conn = create_connection(db_file)

def register(username, password, conn):
    register(username,password,conn)


