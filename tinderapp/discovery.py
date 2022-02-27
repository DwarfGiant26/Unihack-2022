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
        select email,interest
        from Users
        where email != '{email}' 
            and cast(strftime('%Y', 'now') - strftime('%Y', birthday) as int) >= {min_age}
            and cast(strftime('%Y', 'now') - strftime('%Y', birthday) as int) <= {max_age}     
    """
    # and (people_who_like is null or not people_who_like like '%email1%');

    print(sql)
    people = query(sql)

    recommended_list = []
    for person in people:
        for sport in interest.split(','):
            if sport in person[1]:
                recommended_list.append(person)
                break
    
    # filter people that is within age
    # for person in people:
    #     username,other_latitude,other_longitude,description,picture,other_max_radius,interest = person
    #     distance = dist.vincenty((latitude,longitude),(other_latitude,other_longitude)).km
    #     if (max_radius == 'None' or distance < max_radius) and (other_max_radius == 'None' or distance < other_max_radius):
    #         recommended_people.append(person)
    
    # Return a list
    print(recommended_list)
    return recommended_list

def like(likeFrom, likeTo):
    sql = f"""
        UPDATE Users
        SET people_who_like = '{likeFrom}'
        WHERE email = '{likeTo}';   
    """
    execute(sql)


   