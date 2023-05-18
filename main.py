import random
import time
import sys
import serial

from uart import *
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

from Adafruit_IO import MQTTClient

AIO_FEED_ID = [ "fan", "light","cambien1","cambien2","cambien3","mode","music"]
AIO_USERNAME = "NgocKhanh07"
AIO_KEY = "aio_OxaJ94BXNLfMNhbqe7KYaFJ6P4kS"

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe("fan")
    client.subscribe("light")
    client.subscribe("mode")
    client.subscribe("cambien3")
    client.subscribe("cambien1")
    client.subscribe("cambien2")
    client.subscribe("music")
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if feed_id == "fan":
        if payload == "20":
            writeData("1")
        elif payload == "40":
            writeData("2")
        elif payload == "60":
            writeData("3")
        elif payload == "80":
            writeData("4")
        elif payload == "100":
            writeData("5")
        else:
            writeData("6")
    if feed_id == "light":
        if payload == "11":
           writeData("7")
        else:
            writeData("8")
    if feed_id == "mode":
        if payload == "111":
           writeData("9")
        else:
            writeData("10")
    if feed_id == "music":
        if payload == "1":
            writeData("11")
        else:
            writeData("12")

def uart_write(data):
    ser.write((str(data) + "#").encode())
    return

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter_temp = 10
counter_button = 1
while True:
    if(counter_temp <= 0):
        counter_temp = 10
        readSerial(client)
    else:
        counter_temp = counter_temp - 1


    time.sleep(1)