from work_with_DB.requests import connect


def user_create(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = connect.exec_query('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            connect.exec_query(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = connect.exec_query('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                           (email, ))
    except Exception as e:
        raise Exception(e.message)
    return user_describe(user)


def user_details(email):

    user = connect.exec_query('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
    if len(user) == 0:
        return None
    user_describtion = user_describe(user)

    if user_describtion is None:
        raise Exception("No user with email " + email)

    f_list = connect.exec_query(
        'SELECT follower '
        'FROM Followers '
        'JOIN Users ON Users.email = Followers.follower '
        'WHERE followee = %s ',
        (email, )
    )
    user_describtion["followers"] = tuple2list(f_list)

    f_list = connect.exec_query(
        'SELECT followee '
        'FROM Followers '
        'JOIN Users ON Users.email = Followers.followee '
        'WHERE follower = %s ',
        (email, )
    )
    user_describtion["following"] = tuple2list(f_list)

    s_list = []
    subscriptions = connect.exec_query('SELECT thread FROM Subscriptions WHERE user = %s', (email, ))
    for el in subscriptions:
        s_list.append(el[0])
    user_describtion["subscriptions"] = s_list

    return user_describtion


def user_follow(email1, email2):
    connect.is_exist(entity="Users", id="email", value=email1)
    connect.is_exist(entity="Users", id="email", value=email2)
    if email1 == email2:
        raise Exception("User with email=" + email1 + " can't follow himself")
    follows = connect.exec_query(
        'SELECT id '
        'FROM Followers '
        'WHERE follower = %s AND followee = %s',
        (email1, email2, )
    )
    if len(follows) == 0:
        connect.exec_query(
            'INSERT INTO Followers (follower, followee) VALUES (%s, %s)',
            (email1, email2, ))
    user = user_details(email1)
    return user


def user_list_followers_or_following(email, type, params):
    connect.is_exist(entity="Users", id="email", value=email)
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    query = "SELECT "+type+" FROM Followers JOIN Users ON Users.email = Followers."+type+\
            " WHERE "+where+" = %s "
    if "since_id" in params:
        query += " AND Users.id >= "+str(params["since_id"])
    if "order" in params:
        query += " ORDER BY Users.name "+params["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in params:
        query += " LIMIT "+str(params["limit"])
    followers_ids_tuple = connect.exec_query(query=query, params=(email, ))
    f_list = []
    for id in followers_ids_tuple:
        id = id[0]
        f_list.append(user_details(email=id))
    return f_list


def user_unfollow(email1, email2):
    follows = connect.exec_query(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )
    if len(follows) != 0:
        connect.exec_query(
            'DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
        )
    else:
        raise Exception("No such following")
    return user_details(email1)


def user_update_profile(email, about, name):
    connect.is_exist(entity="Users", id="email", value=email)
    connect.exec_query('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
                          (email, about, name, email, ))
    return user_details(email)


def user_describe(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


def tuple2list(list):
    new_list = []
    for el in list:
        new_list.append(el[0])
    return new_list