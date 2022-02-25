from tinderapp.database import execute,query

def register(username, email, password):
    
    sql = f"""
        insert into Users
        values('{username}','{email}','{password}');
    """
    execute(sql)
