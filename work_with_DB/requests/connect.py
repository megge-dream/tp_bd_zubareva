import MySQLdb

def connect_to_db():
    return MySQLdb.connect("localhost", "root", "max", "DBForums", init_command='set names UTF8')


def exec_query(query, params):
    try:
        con = connect_to_db()
        with con:
            cursor = con.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
        con.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Database error in usual query")
    return result


def is_exist(entity, id, value):
    if not len(exec_query('SELECT id FROM ' + entity + ' WHERE ' + id + ' = %s', (value, ))):
        raise Exception("No such element in " + entity + " with " + id + " = " + str(value))
    return