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


def setup_database(database):
    config = configparser.ConfigParser()

    config.read('config/data.ini')
    for key in config['User']:
        user = config['User'][key].split(',')
        register_user(database, user[0], user[1], user[2])

    for key in config['Room']:
        room = config['Room'][key].split(',')
        register_room(database, room[0], room[1], room[2], room[3])

    for key in config['Device']:
        device = config['Device'][key].split(',')
        register_device(database, device[0], device[1], device[2])

    for key in config['Room-Device']:
        devices = config['Room-Device'][key].split(',')
        if len(devices) != 1 and len(devices) != 0:
            for device in devices:
                register_room_device(database, key[1:], device[1:])
        elif len(devices) == 1 and devices[0] != '':
            register_room_device(database, key[1:], devices[0][1:])
        else:
            register_room_device(database, key[1:])

    for key in config['User-Device']:
        devices = config['User-Device'][key].split(',')
        if len(devices) != 1 and len(devices) != 0:
            for device in devices:
                register_user_device(database, key[1:], device[1:])
        elif len(devices) == 1 and devices[0] != '':
            register_user_device(database, key[1:], devices[0][1:])
        else:
            register_user_device(database, key[1:])


def query(database, query, args=(), one=False):
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


def login(database, username):
    user = query(database,
                 'SELECT username, password, role FROM user WHERE username = ?', (username,), one=True)
    return user


def register_user(database, username, password, role='unprivileged'):
    query(database, 'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
          (username, password, role))


def delete_user(username):
    query('DELETE FROM user WHERE username = ?', (username))


def register_device(database, name, operating_period, dev_type):
    query(database, 'INSERT INTO device (name, operating_period, dev_type) VALUES (?, ?, ?)',
          (name, operating_period, dev_type))


def register_room_device(database, room_id, device_id=0):
    query(database, 'INSERT INTO room_device (room_id, device_id) VALUES (?, ?)',
          (room_id, device_id))


def register_user_device(database, user_id, device_id=0):
    query(database, 'INSERT INTO user_device (user_id, device_id) VALUES (?, ?)',
          (user_id, device_id))


def get_lights(database):
    return query(database, 'SELECT * FROM light')


def get_fans(database):
    return query(database, 'SELECT * FROM fan')


def get_modes(database):
    return query(database, 'SELECT * FROM switch')


def get_music_player(database):
    return query(database, 'SELECT * FROM music_player')


def register_room(database, room_type, temperature, humidity, luminance):
    query(database, 'INSERT INTO room (room_type, temperature, humidity, luminance) VALUES (?, ?, ?, ?)',
          (room_type, temperature, humidity, luminance))


def update_room(database, room_id, temperature, humidity, luminance):
    query(database, 'UPDATE room SET temperature = ?, humidity = ?, luminance = ? WHERE id = ?',
          (temperature, humidity, luminance, room_id))


def get_deivce(database, device_id):
    return query(database, 'SELECT * FROM device WHERE id = ?', (device_id,))


def get_user_device(database, user_id):
    device_ids = query(
        database, 'SELECT device_id FROM user_device WHERE user_id = ?', (user_id,))
    devices = []
    for id in device_ids:
        devices.append(get_deivce(database, id['device_id']))
    return devices


def update_fan(database, id, fan_state, rpm, temperature):
    query(database, 'UPDATE fan SET rpm = ?, fan_state = ?, temperature = ? WHERE id = ?',
          (rpm, fan_state, temperature, id))


def update_light(database, id, light_state, brightness, color='#FFFFFF'):
    query(database, 'UPDATE light SET light_state = ?, brightness = ?, color = ? WHERE id = ?',
          (light_state, brightness, color, id))


def update_mode(database, id, mode_state):
    query(database, 'UPDATE switch SET switch_state = ? WHERE id = ?',
          (mode_state, id))


def update_music_player(database, id, mode_state):
    query(database, 'UPDATE music_player SET music_player_state = ? WHERE id = ?',
          (mode_state, id))
