from utils import *
import sqlite3
import configparser
import app


def config_database():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    default_database = config['Database']['database']
    return default_database


def construct_datebase(sql_script, database):
    conn = sqlite3.connect(database)
    with open(sql_script, 'r') as sql_file:
        queries = sql_file.read()
    conn.executescript(queries)
    conn.commit()
    conn.close()


def setup_database():
    pass


def query(database, query, args=(), one=False):
    print(database)
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        if query.startswith('SELECT'):
            try:
                cursor.execute(query, args)
                rv = [dict((cursor.description[idx][0], value)
                           for idx, value in enumerate(row)) for row in cursor.fetchall()]
                return (rv[0] if rv else None) if one else rv
            except sqlite3.IntegrityError as error:
                print(err)
                return None
        else:
            try:
                cursor.execute(query, args)
                conn.commit()
            except sqlite3.IntegrityError as error:
                print(error)
    conn.close()


def login(username, password):
    user = query(
        'SELECT username, password, role FROM user WHERE username = ?', (username,), one=True)
    print(user)


def register(database, username, password, role='unprivileged'):
    query(database, 'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
          (username, password, role))


def delete_user(username):
    query('DELETE FROM user WHERE username = ?', (username))


def register_device(database, name, operating_period, dev_type):
    query(database, 'INSERT INTO device (name, operating_period, dev_type) VALUES (?, ?, ?)',
          (name, operating_period, dev_type))


def delete_device():
    pass


def update_device():
    pass


def register_room():
    pass


def delete_room():
    pass


def update_room():
    pass
