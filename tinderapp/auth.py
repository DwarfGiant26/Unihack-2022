from tinderapp.database import execute,query

def register(username, password, conn):
    sql = f"""
        insert into user
        values('{username}','{password}');
    """
    execute(sql)
