import paho.mqtt.client as mqtt
import time

# Set the Adafruit.io credentials and topic
username = "danh_nguyen"
key = "aio_RTGP18jZ1Pz8ThhSf0cBOEEWOm25"
topic = "{}/feeds/light".format(username)
# Create an MQTT client instance
client = mqtt.Client()

# Set the Adafruit.io credentials
client.username_pw_set(username, key)

# Connect to the Adafruit.io MQTT broker
client.connect("io.adafruit.com", 1883)

# Define a function to update the feed value


def update_feed_value(new_value):
    # Publish the new value to the feed topic
    client.publish(topic, new_value)
    print("Updated feed value to:", new_value)


# Update the feed value to "1" and wait for 5 seconds
update_feed_value("ON")
time.sleep(5)

# Update the feed value to "0" and wait for 5 seconds
update_feed_value("OFF")
time.sleep(5)

# Disconnect from the Adafruit.io MQTT broker
client.disconnect()
