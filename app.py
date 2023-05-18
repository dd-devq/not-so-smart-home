from flask import *
from database import *
from devices import *
import threading
from datetime import datetime

app = Flask(__name__)

default_database = None
sleep_time = 60
username, key, feed_links = None, None, None
sensors = ['cambien1', 'cambien2', 'cambien3']
temperature, lumin, color, humidity = 0, 0, '#FFFFFF', 0
logger_obs, db_obs, mqtt_obs = None, None, None
fan, light, mode, music_player = None, None, None, None
receive = True


def init():
    global default_database, username, key, feed_links, logger_obs, db_obs, mqtt_obs, fan, light, mode, music_player
    database_folder()
    default_database = config_database()
    username, key, feed_links = config_devices()
    construct_datebase('scripts/devices.sql', default_database)
    setup_database(default_database)

    logger_obs = LoggerObserver('log/activities.log')
    db_obs = DatabaseObserver(default_database)
    mqtt_obs = MQTTObserver(username, key)

    light = Light(feed_links[0], '00', 0, '#FFFFFF',
                  [mqtt_obs, logger_obs, db_obs])
    fan = Fan(feed_links[1], 'OFF', '0', temperature,
              [mqtt_obs, logger_obs, db_obs])
    mode = Switch(feed_links[2], '000', [mqtt_obs, logger_obs, db_obs])

    music_player = MusicPlayer(
        feed_links[3], '0', [mqtt_obs, logger_obs, db_obs])


def receiver():
    client = Client(username, key)
    global temperature, lumin, humidity
    while True and receive:
        temperature = client.data(sensors[0])[0].value
        humidity = client.data(sensors[1])[0].value
        lumin = client.data(sensors[2])[0].value
        update_room(default_database, 2,
                    temperature, humidity, lumin)
        time.sleep(20)


def generate_log():
    f = open("log/activities.log", "r")

    log = {}

    light_on_start_time = None
    switch_on_start_time = None
    fan_on_start_time = None
    music_on_start_time = None

    content = f.read().split('\n')[:-1]

    for line in content:
        temp = line.split()
        timestamp = datetime.strptime(
            temp[0] + ' ' + temp[1], '%Y-%m-%d %H:%M:%S.%f')
        device = temp[2]
        state = temp[3]

        if not temp[0] in log:
            log[temp[0]] = {
                'Fan': 0,
                'Light': 0,
                'Switch': 0,
                'Music Player': 0
            }

        if device == 'Light:':
            if state == 'ON':
                light_on_start_time = timestamp
            elif state == 'OFF' and light_on_start_time is not None:
                log[temp[0]]['Light'] += round((timestamp -
                                                light_on_start_time).total_seconds() / 60, 2)
                light_on_start_time = None

        elif device == 'Switch:':
            if state == 'ON':
                switch_on_start_time = timestamp
            elif state == 'OFF' and switch_on_start_time is not None:
                log[temp[0]]['Switch'] += round((timestamp -
                                                 switch_on_start_time).total_seconds() / 60, 2)
                switch_on_start_time = None

        elif device == 'MusicPlayer:':
            if state == 'ON':
                music_on_start_time = timestamp
            elif state == 'OFF' and music_on_start_time is not None:
                log[temp[0]]['Music Player'] += round((timestamp -
                                                       music_on_start_time).total_seconds() / 60, 2)
                music_on_start_time = None

        elif device == 'Fan:':
            temp_fan = state.split(',')
            sub_state = temp_fan[1]

            if 'ON' in sub_state:
                fan_on_start_time = timestamp
            elif 'OFF' in sub_state and fan_on_start_time is not None:
                log[temp[0]]['Fan'] += round((timestamp -
                                              fan_on_start_time).total_seconds() / 60, 2)
                fan_on_start_time = None
    return log


@ app.route('/')
def home():
    return 'Home'


@ app.route('/receiver/on')
def receiver_on():
    global receive
    receive = True
    return 'Receiver on'


@ app.route('/receiver/off')
def receiver_off():
    global receive
    receive = False
    return 'Receiver off'


@ app.route('/sensor', methods=['GET'])
def sensor():
    data = [temperature, humidity, lumin]
    return jsonify(data)


@ app.route('/light', methods=['GET'])
def lights():
    return jsonify(get_lights(default_database))

@ app.route('/fan', methods=['GET'])
def fans():
    return jsonify(get_fans(default_database))

@ app.route('/mode', methods=['GET'])
def modes():
    return jsonify(get_modes(default_database))

@ app.route('/music_player', methods=['GET'])
def music_player():
    return jsonify(get_music_player(default_database))

@ app.route('/user/<string:username>', methods=['GET'])
def user(username):
    return jsonify(login(default_database, username))


@ app.route('/light/on')
def light_on():
    light.light_on(lumin, color)

    return 'Turn light on'


@ app.route('/light/off')
def light_off():
    light.light_off()
    return 'Turn light off'


@ app.route('/fan/on')
def fan_on():
    speed = request.args.get('speed')
    fan.fan_on(speed, temperature)
    return 'Turn fan on'


@ app.route('/fan/off')
def fan_off():
    fan.fan_off(temperature)
    return 'Turn fan off'


@ app.route('/mode/on')
def switch_on():
    mode.switch_on()
    return 'Turn mode on'


@ app.route('/mode/off')
def switch_off():
    mode.switch_off()
    return 'Turn mode off'


@ app.route('/music/on')
def music_on():
    music_player.music_on()
    return 'Turn music on'


@ app.route('/music/off')
def music_off():
    music_player.music_off()
    return 'Turn music off'


@ app.route('/user/<int:id>/devices')
def user_device(id):
    return jsonify(get_user_device(default_database, id))


@ app.route('/log/')
def log():
    return jsonify(generate_log())


if __name__ == "__main__":
    init()
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_evalex=False)


@ app.errorhandler(404)
def not_found(error):
    return response('404 Not Found'), 404


@ app.errorhandler(403)
def forbidden(error):
    return response('403 Forbidden'), 403


@ app.errorhandler(400)
def bad_request(error):
    return response('400 Bad Request'), 400


@ app.errorhandler(Exception)
def handle_error(error):
    message = error.description if hasattr(error, 'description') else [
        str(x) for x in error.args]
    response = {
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return response, error.code if hasattr(error, 'code') else 500
