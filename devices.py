from Adafruit_IO import Client, Feed, RequestError
import paho.mqtt.client as mqtt
import sqlite3
import time
import configparser
from datetime import datetime
import database


class Observer():
    def update(self, feed, status=()):
        pass


class DatabaseObserver(Observer):
    def __init__(self, database):
        self.database = database

    def update(self, feed, status=()):

        stat = status[0]
        if len(status) > 1:
            val_1 = status[1]
            val_2 = status[2]
        if 'light' in feed:
            database.update_light(self.database, 1, stat, val_1, val_2)
        if 'fan' in feed:
            database.update_fan(self.database, 1, stat, val_1, val_2)
        if 'mode' in feed:
            database.update_mode(self.database, 1, stat)


class MQTTObserver(Observer):
    def __init__(self, username, key):
        self.username = username
        self.key = key
        self.client = mqtt.Client()
        self.client.username_pw_set(username, key)
        self.client.connect("io.adafruit.com", 1883)

    def update(self, feed, status=()):
        stat = status[0]
        result = self.client.publish(feed, stat)
        time.sleep(0.1)


class LoggerObserver(Observer):
    def __init__(self, log_file):
        self.log_file = log_file

    def update(self, feed, status=()):
        stat = status[0]
        if len(status) > 1:
            val_1 = status[1]
            val_2 = status[2]
        log = open(self.log_file, 'a')
        device = None
        if 'light' in feed:
            device = ' Light: '
        if 'fan' in feed:
            device = ' Fan: ' + str(status)
            log.write(str(datetime.now()) + device + '\n')
            return
        if 'mode' in feed:
            device = ' Switch: '
        temp = None
        if '0' in stat:
            temp = 'OFF'
        if '1' in stat:
            temp = 'ON'
        log.write(str(datetime.now()) + device + temp + '\n')


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
    def __init__(self, feed, status="00", lumin=0, color='#FFFFFF', observers=[]):
        super().__init__(feed, observers)
        self.status = status
        self.lumin = lumin
        self.color = color

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.feed, (self.status, self.lumin, self.color))

    def light_off(self):
        self.status = '00'
        self.lumin = 0
        self.notify()

    def light_on(self, lumin, color='#FFFFFF'):
        self.status = '11'
        self.lumin = lumin
        self.color = color
        self.notify()


class Fan(Device):
    def __init__(self, feed, status='OFF', speed='0', temperature=0, observers=[]):
        super().__init__(feed, observers)
        self.status = status
        self.speed = speed
        self.temperature = temperature

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(
                self.feed, (self.status, self.speed, self.temperature))

    def fan_off(self, temperature):
        self.speed = '0'
        self.temperature = temperature
        self.status = 'OFF'
        self.notify()

    def fan_on(self, speed, temperature):
        self.status = 'ON'
        self.temperature = temperature
        self.speed = speed
        self.notify()


class Switch(Device):
    def __init__(self, feed, status='000', observers=[]):
        super().__init__(feed, observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.feed, (self.status,))

    def switch_off(self):
        self.status = '000'
        self.notify()

    def switch_on(self):
        self.status = '111'
        self.notify()


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
