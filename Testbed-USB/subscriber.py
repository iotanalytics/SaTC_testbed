# subscriber.py

import paho.mqtt.client as mqtt
import sys
from pathlib import Path

p = Path('.')

# from motorchange import motorchange

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(f"raspberry/sensorweb{sys.argv[1]}")
    print("channel is ",sys.argv[1])
    #client.subscribe(f"raspberry/sensorweb{chn}")

def on_message(client, userdata, msg):
    motor_command = str(msg.payload.decode("utf-8"))
    command_file = open(f"motor_command{sys.argv[1]}.txt", "w")
    #command_file = open(f"motor_command{chn}.txt", "w")
    print("motor_command = ",motor_command)
    print("sys arg 1 is ", sys.argv[1])
    command_file.write(motor_command)
    command_file.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#print(status)
client.will_set('raspberry/status',  b'{"status": "Off"}')

client.connect("broker.emqx.io", 1883, 60)

client.loop_forever()