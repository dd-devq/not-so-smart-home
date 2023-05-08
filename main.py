import random
import time
import sys
import serial

from uart import *
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

from Adafruit_IO import MQTTClient

AIO_FEED_ID = [ "nutnhan1", "nutnhan2","cambien1","cambien2","cambien4","nutnhan3"]
AIO_USERNAME = "NgocKhanh07"
AIO_KEY = "aio_gnKY52bhnuz8VsMgvMJHNW1R68Tw"

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe("nutnhan1")
    client.subscribe("nutnhan2")
    client.subscribe("nutnhan3")
    # client.subscribe("cambien1")
    # client.subscribe("cambien2")
    client.subscribe("cambien4")


def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if feed_id == "nutnhan1":
        if payload == "11":
            writeData("1")
        else:
            writeData("2")
    if feed_id == "nutnhan2":
        if payload == "1":
           writeData("3")
        else:
            writeData("4")
    if feed_id == "nutnhan3":
        if payload == "111":
           writeData("5")
        else:
            writeData("6")

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

counter_1 = 10
counter_2 = 5
counter_3 = 1
while True:

    readSerial(client)
    time.sleep(1)
