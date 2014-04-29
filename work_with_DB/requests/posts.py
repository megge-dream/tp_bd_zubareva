from work_with_DB.requests import users, threads, forums, connect
from work_with_DB.requests.connect import connect_to_db


def post_create(date, thread, message, user, forum, optional_params):
    connect.is_exist(entity="Threads", id="id", value=thread)
    connect.is_exist(entity="Forums", id="short_name", value=forum)
    connect.is_exist(entity="Users", id="email", value=user)
    if len(connect.exec_query(
            "SELECT Threads.id "
            "FROM Threads "
            "JOIN Forums ON Threads.forum = Forums.short_name "
            "WHERE Threads.forum = %s AND Threads.id = %s",
            (forum, thread, )
    )) == 0:
        raise Exception("thread with id = " + thread + " in forum " + forum + " not found ")
    if "parent" in optional_params:
        if len(connect.exec_query(
                "SELECT Posts.id "
                "FROM Posts "
                "JOIN Threads ON Threads.id = Posts.thread "
                "WHERE Posts.id = %s AND Threads.id = %s",
                (optional_params["parent"], thread, )
        )) == 0:
            raise Exception("post with id = " + optional_params["parent"] + " not found ")
    query_for_ins = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    params = [message, user, forum, thread, date]

    for param in optional_params:
        query_for_ins += ", "+param
        values += ", %s"
        params.append(optional_params[param])
    query_for_ins += ") VALUES " + values + ")"
    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"
    con = connect_to_db()
    con.autocommit(False)
    with con:
        cursor = con.cursor()
        try:
            con.begin()
            cursor.execute(update_thread_posts, (thread, ))
            cursor.execute(query_for_ins, params)
            con.commit()
        except Exception as e:
            con.rollback()
            raise Exception("Database error: " + e.message)
        id = cursor.lastrowid
        cursor.close()
    con.close()

    post = connect.exec_query(
        'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
            'isHighlighted, isSpam, likes, message, parent, points, thread, user '
        'FROM Posts '
        'WHERE id = %s',
        (id, )
    )
    if len(post) == 0:
        post_describtion = None
    else:
        post_describtion = post_describe(post)

    del post_describtion["dislikes"]
    del post_describtion["likes"]
    del post_describtion["parent"]
    del post_describtion["points"]
    return post_describtion


def post_details(id, related):
    post = connect.exec_query(
        'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
            'isHighlighted, isSpam, likes, message, parent, points, thread, user '
        'FROM Posts '
        'WHERE id = %s',
        (id, )
    )
    if len(post) == 0:
        post_describtion = None
    else:
        post_describtion = post_describe(post)

    if post_describtion is None:
        raise Exception("no post with id = "+id)
    if "user" in related:
        post_describtion["user"] = users.user_details(post_describtion["user"])
    if "forum" in related:
        post_describtion["forum"] = forums.forum_details(short_name=post_describtion["forum"], related=[])
    if "thread" in related:
        post_describtion["thread"] = threads.thread_details(id=post_describtion["thread"], related=[])
    return post_describtion


def post_list(entity, id, related, params):
    if entity == "user":
        connect.is_exist(entity="Users", id="email", value=id)

    if entity == "forum":
        connect.is_exist(entity="Forums", id="short_name", value=id)

    if entity == "thread":
        connect.is_exist(entity="Threads", id="id", value=id)

    query = "SELECT id FROM Posts WHERE " + entity + " = %s "
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
    post_ids = connect.exec_query(query=query, params=parameters)
    post_list = []
    for id in post_ids:
        id = id[0]
        post_list.append(post_details(id=id, related=related))
    return post_list


def post_remove(post_id):
    connect.is_exist(entity="Posts", id="id", value=post_id)
    connect.exec_query(
        "UPDATE Posts "
        "SET isDeleted = 1 "
        "WHERE Posts.id = %s",
        (post_id, )
    )
    return {
        "post": post_id
    }


def post_restore(post_id):
    connect.is_exist(entity="Posts", id="id", value=post_id)
    connect.exec_query(
        "UPDATE Posts "
        "SET isDeleted = 0 "
        "WHERE Posts.id = %s",
        (post_id, )
    )
    return {
        "post": post_id
    }

def post_update(id, message):
    connect.is_exist(entity="Posts", id="id", value=id)
    connect.exec_query(
        'UPDATE Posts '
        'SET message = %s '
        'WHERE id = %s',
        (message, id, )
    )
    return post_details(id=id, related=[])


def post_vote(id, vote):
    connect.is_exist(entity="Posts", id="id", value=id)
    if vote == -1:
        connect.exec_query(
            "UPDATE Posts "
            "SET dislikes=dislikes+1, points=points-1 "
            "WHERE id = %s",
            (id, )
        )
    else:
        connect.exec_query(
            "UPDATE Posts "
            "SET likes=likes+1, points=points+1  "
            "WHERE id = %s",
            (id, )
        )
    return post_details(id=id, related=[])


def post_describe(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],

    }
    return post_response
