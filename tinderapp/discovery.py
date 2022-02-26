from tinderapp.database import execute,query
from geopy import distance as dist

# given email, we want to return list of people who fulfill the preference criteria of this user
def list_recommended_people(email):
    # get preference and location
    sql = f"""
        select latitude,longitude,max_radius,interest,min_age,max_age
        from Users
        where email='{email}';
    """
    latitude,longitude,max_radius,interest,min_age,max_age = query(sql)[0]
    
    # get people within interest and age preference
    sql = f"""
        select username,latitude,longitude,description,picture,max_radius,interest,birthday
        from Users
        where interest like '%{interest}%' 
            and email != '{email}' 
            and cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', dob) as int) >= min_age
            and cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', dob) as int) <= max_age
            and not people_who_like like '%{email}%';
    """
    people = query(sql)

    recommended_people = people

    # filter people that is within age
    # for person in people:
    #     username,other_latitude,other_longitude,description,picture,other_max_radius,interest = person
    #     distance = dist.vincenty((latitude,longitude),(other_latitude,other_longitude)).km
    #     if (max_radius == 'None' or distance < max_radius) and (other_max_radius == 'None' or distance < other_max_radius):
    #         recommended_people.append(person)
    
    return recommended_people