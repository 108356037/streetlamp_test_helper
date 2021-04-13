#!/usr/bin/env python
from paho.mqtt import client as mqtt_client
import json
import yaml
from datetime import datetime
import time
import os
import random
import signal
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--interval", help="the interval time (sec) between commands", type=int)

args = parser.parse_args()


def signal_handler(sig, frame):
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
    
def on_publish(client,userdata,result):
    print('time: ',datetime.now().strftime("%H:%M:%S"))
    print(f" {client} published {userdata}, result: {result}")

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Gracefully disconnected.")
    else:
        print("Unexpected disconnection.")

mqttc_id = 'debug:debug-client:'+ str(random.randint(0,9999))

client = mqtt_client.Client(client_id=mqttc_id)
client.username_pw_set("debug","debug")
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect


client.connect("broker.insynerger.streetlightbroker.com", 4883, 60)
client.loop_start()



with open('cmd.yaml') as file:
    documents = yaml.full_load(file)
    for cmd, val in documents['info'].items():
        print(f"testing -> cmd: {cmd}, val: {val}")
        if val == "" :
            payload = {
                "type": cmd
            }
        else:
            payload = {
                "type": cmd,
                "value": val
            }

        client.publish("$thing/OR000000insynerger05/$cmd/conf/info",json.dumps(payload),qos=1).wait_for_publish()
        time.sleep(args.interval)

client.loop_stop()
client.disconnect()
sys.exit(0)