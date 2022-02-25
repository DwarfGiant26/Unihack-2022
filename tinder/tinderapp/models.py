from django.db import models
from matplotlib.pyplot import connect
from database import create_connection
from register import register

db_file = "../db.sqlite3"
# Create your models here.

conn = create_connection(db_file)

