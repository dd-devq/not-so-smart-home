from flask import *
from database import *
from devices import *
import threading

app = Flask(__name__)

default_database = None
sleep_time = 10
username, key, feed_links = None, None, None
logger_obs, db_obs, mqtt_obs = None, None, None
devices = {
    'light': [],
    'fan': [],
    'humansensor': []
}


def init():
    global default_database, username, key, feed_links, logger_obs, db_obs, mqtt_obs, devices
    database_folder()
    default_database = config_database()
    username, key, feed_links = config_devices()
    construct_datebase('scripts/devices.sql', default_database)
    setup_database(default_database)

    logger_obs = LoggerObserver('log/activities.log')
    db_obs = DatabaseObserver()
    mqtt_obs = MQTTObserver(username, key)
    devices = {
        'light': [],
        'fan': [],
        'humansensor': []
    }
    for feed in feed_links:
        if 'light' in feed:
            devices['light'].append(
                Light(feed, 'OFF', [mqtt_obs, logger_obs, db_obs]))
        elif 'fan' in feed:
            devices['fan'].append(
                Fan(feed, 'OFF', [mqtt_obs, logger_obs, db_obs]))
        elif 'humansensor' in feed:
            devices['humansensor'].append(
                HumanSensor(feed, 'OFF', [mqtt_obs, logger_obs, db_obs]))


def on_message(client, userdata, message):
    global sleep_time
    sleep_time = 10
    value = message.payload.decode('utf-8')
    print(f'Received message: {value}')


def on_connect(client, userdata, flags, rc):

    for feed in feed_links:
        client.subscribe(feed)


def receiver():
    client = mqtt.Client()
    client.username_pw_set(username, key)
    client.connect("io.adafruit.com", 1883)
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_start()
    time.sleep(sleep_time)
    client.loop_stop()


@app.route('/')
def test():
    devices['light'][0].light_on()
    return 'testing'


if __name__ == "__main__":
    init()
    # receiver_thread = threading.Thread(target=receiver)
    # receiver_thread.start()
    # app.run(host='0.0.0.0', port=5000, debug=False, use_evalex=False)


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
