from tinderapp.database import execute,query

def register(username, email, password):
    sql = f"""
        insert into Users
        values('{username}','{email}','{password}');
    """
    execute(sql)

def check_password(email,password):
    sql = f"""
        select *
        from Users
        where email='{email}' and password='{password}';
    """
    if len(query(sql)) == 0:
        return False
    return True

