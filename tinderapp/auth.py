from tinderapp.database import execute,query

def register(username, email, password):
    
    sql = f"""
        insert into Users
        values('{username}','{email}','{password}');
    """
    execute(sql)

    sql = """
        SELECT 
            name
        FROM 
            sqlite_schema
        WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%';
    """
    print(query(sql))
