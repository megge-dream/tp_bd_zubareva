from work_with_DB.requests import users, connect


def forum_create(name, short_name, user):
    connect.is_exist(entity="Users", id="email", value=user)
    forum = connect.exec_query(
        'SELECT id, name, short_name, user '
        'FROM Forums '
        'WHERE short_name = %s',
        (short_name, )
    )
    if len(forum) == 0:
        connect.exec_query(
            'INSERT INTO Forums (name, short_name, user) '
            'VALUES (%s, %s, %s)',
            (name, short_name, user, )
        )
        forum = connect.exec_query(
            'SELECT id, name, short_name, user '
            'FROM Forums '
            'WHERE short_name = %s',
            (short_name, )
        )
    return forum_description(forum)


def forum_details(short_name, related):
    forum = connect.exec_query(
        'SELECT id, name, short_name, user '
        'FROM Forums '
        'WHERE short_name = %s',
        (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with short_name=" + short_name)
    forum = forum_description(forum)

    if "user" in related:
        forum["user"] = users.user_details(forum["user"])
    return forum


def forum_list_users(short_name, optional):
    connect.is_exist(entity="Forums", id="short_name", value=short_name)

    query = "SELECT distinct email " \
            "FROM Users " \
            "JOIN Posts ON Posts.user = Users.email " \
            " JOIN Forums on Forums.short_name = Posts.forum " \
            "WHERE Posts.forum = %s "
    if "since_id" in optional:
        query += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    users_tuple = connect.exec_query(query, (short_name, ))
    list = []
    for user in users_tuple:
        user = user[0]
        list.append(users.user_details(user))
    return list


def forum_description(forum):
    forum = forum[0]
    forum_response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return forum_response