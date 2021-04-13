#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime
import random
import signal
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--topic", help="the mqtt topic to subscribe", type=str)
parser.add_argument("--qos", help="the QOS of MQTT message", type=int)

args = parser.parse_args()

print('Proccess id:', os.getpid())

WRITE_FLAG = False
#MQTT_TOPIC = [("$thing/OR000000insynerger05/$data/conf/#",1)]
MQTT_TOPIC = [(args.topic,args.qos)]
print(MQTT_TOPIC)

def signal_handler(sig, frame):
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe(MQTT_TOPIC)
    

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print('time: ',datetime.now().strftime("%H:%M:%S"))
    print(msg.topic + "||" + str(msg.payload)+'\n')

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Gracefully disconnected.")
    else:
        print("Unexpected disconnection.")

mqttc_id = 'debug:debug-client:'+ str(random.randint(0,9999))
print('MQTT-client-id:', mqttc_id)

client = mqtt.Client(client_id=mqttc_id)
client.username_pw_set("debug","debug")

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("broker.insynerger.streetlightbroker.com", 4883, 60)
client.loop_forever()