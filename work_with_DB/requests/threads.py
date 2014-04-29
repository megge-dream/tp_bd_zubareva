from work_with_DB.requests import users, forums, connect


def thread_close(id):
    connect.is_exist(entity="Threads", id="id", value=id)
    connect.exec_query(
        "UPDATE Threads "
        "SET isClosed = 1 "
        "WHERE id = %s",
        (id, )
    )
    response = {
        "thread": id
    }
    return response


def thread_create(forum, title, isClosed, user, date, message, slug, optional):
    connect.is_exist(entity="Users", id="email", value=user)
    connect.is_exist(entity="Forums", id="short_name", value=forum)
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = connect.exec_query(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(thread) == 0:
        connect.exec_query(
            'INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, isClosed, user, date, message, slug, isDeleted, )
        )
        thread = connect.exec_query(
            'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    response = thread_description(thread)
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]
    return response


def thread_details(id, related):
    thread = connect.exec_query(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )
    if len(thread) == 0:
        raise Exception('No thread exists with id=' + str(id))
    thread = thread_description(thread)
    if "user" in related:
        thread["user"] = users.user_details(thread["user"])
    if "forum" in related:
        thread["forum"] = forums.forum_details(short_name=thread["forum"], related=[])
    return thread


def threads_list(entity, id, related, params):
    if entity == "forum":
        connect.is_exist(entity="Forums", id="short_name", value=id)
    if entity == "user":
        connect.is_exist(entity="Users", id="email", value=id)
    query = "SELECT id FROM Threads WHERE " + entity + " = %s "
    parameters = [id]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    thread_ids_tuple = connect.exec_query(query=query, params=parameters)
    thread_list = []
    for id in thread_ids_tuple:
        id = id[0]
        thread_list.append(thread_details(id=id, related=related))
    return thread_list


def thread_open(id):
    connect.is_exist(entity="Threads", id="id", value=id)
    connect.exec_query(
        "UPDATE Threads SET isClosed = 0 "
        "WHERE id = %s",
        (id, )
    )
    response = {
        "thread": id
    }
    return response


def thread_remove(thread_id):
    connect.is_exist(entity="Threads", id="id", value=thread_id)
    connect.exec_query(
        "UPDATE Threads SET isDeleted = 1 "
        "WHERE id = %s",
        (thread_id, )
    )
    response = {
        "thread": thread_id
    }
    return response


def thread_restore(thread_id):
    connect.is_exist(entity="Threads", id="id", value=thread_id)
    connect.exec_query(
        "UPDATE Threads SET isDeleted = 0 "
        "WHERE id = %s",
        (thread_id, )
    )
    response = {
        "thread": thread_id
    }
    return response


def thread_subscribe(email, thread_id):
    connect.is_exist(entity="Threads", id="id", value=thread_id)
    connect.is_exist(entity="Users", id="email", value=email)
    subscription = connect.exec_query(
        'SELECT thread, user '
        'FROM Subscriptions '
        'WHERE user = %s AND thread = %s',
        (email, thread_id, )
    )
    if len(subscription) == 0:
        connect.exec_query(
            'INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, )
        )
        subscription = connect.exec_query(
            'SELECT thread, user '
            'FROM Subscriptions '
            'WHERE user = %s AND thread = %s',
            (email, thread_id, )
        )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def thread_unsubscribe(email, thread_id):
    connect.is_exist(entity="Threads", id="id", value=thread_id)
    connect.is_exist(entity="Users", id="email", value=email)
    subscription = connect.exec_query(
        'SELECT thread, user '
        'FROM Subscriptions '
        'WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    connect.exec_query(
        'DELETE FROM Subscriptions '
        'WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def thread_update(id, slug, message):
    connect.is_exist(entity="Threads", id="id", value=id)
    connect.exec_query('UPDATE Threads SET slug = %s, message = %s WHERE id = %s',
                          (slug, message, id, ))
    return thread_details(id=id, related=[])


def thread_vote(id, vote):
    connect.is_exist(entity="Threads", id="id", value=id)
    if vote == -1:
        connect.exec_query(
            "UPDATE Threads SET dislikes=dislikes+1, points=points-1 "
            "WHERE id = %s",
            (id, )
        )
    else:
        connect.exec_query(
            "UPDATE Threads SET likes=likes+1, points=points+1  "
            "WHERE id = %s",
            (id, )
        )
    return thread_details(id=id, related=[])


def thread_description(thread):
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }
    return response