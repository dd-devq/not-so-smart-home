from Adafruit_IO import Client, Feed, RequestError
import paho.mqtt.client as mqtt
import sqlite3
import time
username = 'danh_nguyen'
key = 'aio_RTGP18jZ1Pz8ThhSf0cBOEEWOm25'

feeds = [
    '{}/feeds/light'.format(username),
    '{}/feeds/fan'.format(username),
    '{}/feeds/humansensor'.format(username)
]


class Observer():
    def update(self, status):
        pass


class DatabaseObserver(Observer):
    def __init__(self):
        pass

    def update(self, status):
        print(f"Database Updated: {status}")


class MQTTObserver(Observer):
    def __init__(self, username, key):
        self.username = username
        self.key = key
        self.client = mqtt.Client()
        self.client.username_pw_set(username, key)
        self.client.connect("io.adafruit.com", 1883)

    def add_topic(topic):
        pass

    def update(self, feed, status):
        msg_count = 0
        result = self.client.publish(feed, status)
        stat = result[0]
        if stat == 0:
            print(f"Send `{status}` to topic `{feed}`")
        else:
            print(f"Failed to send message to feed {feed}")


class LoggerObserver(Observer):
    def __init__(self):
        pass

    def update(self, status):
        print(f"Observer Updated: {status}")


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
    list_feed = ['Feed/Light']
    pass


def setup():
    pass


if __name__ == '__main__':
    db_obs = DatabaseObserver()
    mqtt_obs = MQTTObserver(username, key)
    light_device = Light('danh_nguyen/feeds/light', 'OFF', [mqtt_obs])
    fan_device = Fan('danh_nguyen/feeds/fan', 'OFF', [mqtt_obs])
    human_sensor_device = HumanSensor(
        'danh_nguyen/feeds/humansensor', 'OFF', [mqtt_obs])
    light_device.light_on()
    fan_device.fan_on()
    human_sensor_device.human_sensor_on()
