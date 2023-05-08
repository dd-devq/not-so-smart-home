from Adafruit_IO import Client, Feed, RequestError
import paho.mqtt.client as mqtt

username = 'NgocKhanh07'
key = 'aio_gnKY52bhnuz8VsMgvMJHNW1R68Tw'
client = mqtt.Client()
client.username_pw_set(username, key)
client.connect("io.adafruit.com", 1883)

feed = 'NgocKhanh07/feeds/fan'
result = client.publish(feed, '0')
stat = result[0]
if stat == 0:
    print(f"Send `1` to topic `{feed}`")
else:
    print(f"Failed to send message to feed {feed}")
