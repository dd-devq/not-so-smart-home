from Adafruit_IO import Client, Feed, RequestError
import paho.mqtt.client as mqtt
import sqlite3
import time
import configparser
from datetime import datetime


class Observer():
    def update(self, status):
        pass


class DatabaseObserver(Observer):
    def __init__(self):
        pass

    def update(self, feed, status):
        print(f"Database Updated: {status}")


class MQTTObserver(Observer):
    def __init__(self, username, key):
        self.username = username
        self.key = key
        self.client = mqtt.Client()
        self.client.username_pw_set(username, key)
        self.client.connect("io.adafruit.com", 1883)

    def update(self, feed, status):
        result = self.client.publish(feed, status)
        time.sleep(0.1)
        stat = result[0]
        if stat == 0:
            print(f"Send `{status}` to topic `{feed}`")
        else:
            print(f"Failed to send message to feed {feed}")


class LoggerObserver(Observer):
    def __init__(self, log_file):
        self.log_file = log_file

    def update(self, feed, status):
        log = open(self.log_file, 'a')
        log.write(str(datetime.now()) + '\n')


class Device():
    def __init__(self, feed, observers=[]):
        self.observers = observers
        self.feed = feed

    def attach(self, observer):
        pass

    def dettach(self, observer):
        pass

    def notify(self):
        pass


class Light(Device):
    def __init__(self, feed, status="OFF", observers=[]):
        super().__init__(feed, observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.feed, self.status)

    def light_off(self):
        self.status = 'OFF'
        self.notify()

    def light_on(self):
        self.status = 'ON'
        self.notify()


class Fan(Device):
    def __init__(self, feed, status='OFF', observers=[]):
        super().__init__(feed, observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.feed, self.status)

    def fan_off(self):
        self.status = 'OFF'
        self.notify()

    def fan_on(self):
        self.status = 'ON'
        self.notify()


class HumanSensor(Device):
    def __init__(self, feed, status='OFF', observers=[]):
        super().__init__(feed, observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.feed, self.status)

    def human_sensor_off(self):
        self.status = 'OFF'
        self.notify()

    def human_sensor_on(self):
        self.status = 'ON'
        self.notify()


class SystemRecord:
    key = 'aio_RTGP18jZ1Pz8ThhSf0cBOEEWOm25'
    pass


def config_devices():
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    username = config['Adafruit']['username']
    key = config['Adafruit']['key']

    feeds = config['Adafruit']['feeds'].split(',')

    feed_prefix = username + '/feeds/'
    feed_links = []
    for feed in feeds:
        feed_links.append(feed_prefix + feed)

    return username, key, feed_links
