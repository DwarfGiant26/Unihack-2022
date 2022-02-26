from tinderapp.database import execute,query
from geopy import distance as dist

# given email, we want to return list of people who fulfill the preference criteria of this user
def list_recommended_people(email):
    # get preference and location
    sql = f"""
        select latitude,longitude,max_radius,interest
        from Users
        where email='{email}';
    """
    latitude,longitude,max_radius,interest = query(sql)[0]
    
    # get people within interest preference
    sql = f"""
        select username,latitude,longitude,description,picture,max_radius,interest,birthday
        from Users
        where interest like '%{interest}%' and email != '{email}';
    """
    people = query(sql)

    recommended_list = []
    # filter people that is within distance and age
    for person in people:
        username,other_latitude,other_longitude,description,picture,other_max_radius,interest = person
        distance = dist.vincenty((latitude,longitude),(other_latitude,other_longitude)).km
        if (max_radius == 'None' or distance < max_radius) and (other_max_radius == 'None' or distance < other_max_radius):
            recommended_list.append(person)
    
    # Return a list
    recommended_people = ",".join(str(x) for x in recommended_list)
    return recommended_people

def like(likeFrom, likeTo):
    sql = f"""
        UPDATE Users
        SET people_who_like = '{likeFrom}'
        WHERE email = '{likeTo}';   
    """
    execute(sql)


   