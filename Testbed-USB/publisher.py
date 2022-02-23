import paho.mqtt.client as mqtt
import time
import sys
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

client.publish(f'raspberry/sensorweb{sys.argv[1]}', payload=sys.argv[2], qos=0, retain=False)
print(f"send {sys.argv[1]} to raspberry/topic")
#time.sleep(1)
quit()


