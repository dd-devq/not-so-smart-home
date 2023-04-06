from Adafruit_IO import Client, Feed, RequestError
import paho.mqtt.client as mqtt
import sqlite3


class Observer():
    def update(self, status):
        pass


class DatabaseObserver(Observer):
    def __init__(self):
        pass

    def update(self, status):
        print(f"Database Updated: {status}")


class MQTTObserver(Observer):
    def __init__(self):
        pass

    def update(self, status):
        print(f"MQTT Updated: {status}")


class Device():
    def __init__(self, observers=[]):
        self.observers = observers

    def attach(self, observer):
        pass

    def dettach(self, observer):
        pass

    def notify(self):
        pass


class Light(Device):
    def __init__(self, status=False, observers=[]):
        super().__init__(observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.status)

    def light_off(self):
        self.status = False
        self.notify()

    def light_on(self):
        self.status = True
        self.notify()


class Fan(Device):
    def __init__(self, status=False, observers=[]):
        super().__init__(observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.status)

    def fan_off(self):
        self.status = False
        self.notify()

    def fan_on(self):
        self.status = True
        self.notify()


class HumanSensor(Device):
    def __init__(self, status=False, observers=[]):
        super().__init__(observers)
        self.status = status

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.status)

    def human_sensor_off(self):
        self.status = False
        self.notify()

    def human_sensor_on(self):
        self.status = True
        self.notify()


if __name__ == '__main__':
    db_obs = DatabaseObserver()
    mqtt_obs = MQTTObserver()
    light_device = Light(False, [db_obs, mqtt_obs])
    fan_device = Fan(False, [db_obs, mqtt_obs])
    human_sensor_device = HumanSensor(False, [db_obs, mqtt_obs])

    light_device.light_on()
    fan_device.fan_on()
    human_sensor_device.human_sensor_on()
