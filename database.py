from utils import *
import sqlite3

default_database = 'database/devices.db'


def construct_datebase(sql_script, database=default_database):
    global default_database
    default_database = database
    conn = sqlite3.connect(database)
    with open(sql_script, 'r') as sql_file:
        queries = sql_file.read()
        print(queries)
    conn.executescript(queries)
    conn.commit()
    conn.close()


def query(query, args=(), one=False):
    with sqlite3.connect(default_database) as conn:
        cursor = conn.cursor()
        if query.startswith('SELECT'):
            cursor.execute(query, args)
            rv = [dict((cursor.description[idx][0], value)
                       for idx, value in enumerate(row)) for row in cursor.fetchall()]
            return (rv[0] if rv else None) if one else rv
        else:
            cursor.execute(query, args)
            conn.commit()


def login(username, password):
    user = query(
        'SELECT username, password, role FROM user WHERE username = ?', (username,), one=True)
    print(user)


def register(username, password, role='unprivileged'):
    query('INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
          (username, password, role))


def delete_user(username):
    query('DELETE FROM user WHERE username = ?', (username,))
