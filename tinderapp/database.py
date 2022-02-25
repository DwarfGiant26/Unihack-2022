import sqlite3

db_file = "../db.sqlite3"

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def execute(sql):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    
def query(sql):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    except Exception as e:
        print(e)
        return e

    conn.close()
    return rows