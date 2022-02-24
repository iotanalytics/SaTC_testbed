#! stdbuf -i0 -oL -e0 tshark -i wlx00c0ca5fb01e -q -T fields -e frame.time_relative -e _ws.col.Protocol -e eth.src -e eth.dst -e _ws.col.Length -e  _ws.col.Info | python /home/sensorweb/NetworkData.py

import sys
import datetime
from influxdb import InfluxDBClient
number = 0
client = InfluxDBClient(host = 'localhost', port = 8086)
client.switch_database("NetworkData")

currentTime = datetime.datetime.now()
timestamp = int(currentTime.timestamp()*1000000000)

### start a timer here refer: https://github.com/SongClass/SimTCP 
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
         
def dummyfn(msg="foo"):
    print(msg)

    for something in sys.stdin:
        packet = something.split()
        print(packet)
        time = int(float(packet[0]))
        protocol = str(packet[1])
        if protocol == 'ARP':
            number += 1
        else:
            if number > 0:
               number = 0
        source_MAC_Address = packet[2]
        length = int(packet[4])
        dst_MAC_Address = packet[3]
        ttt = timestamp + int(round(time)*1000000000)
        infor = ""
        for i in range(5, len(packet)):
            infor += "" + packet[i] + " "

        traffic =   length*number
        json_body = [
            {
                "measurement": "NetworkData",
                "tags": {
                    "Information":infor,
                    "Protocol":protocol,
                    "Source": source_MAC_Address,
                    "Destination": dst_MAC_Address
                },
                "fields":{
                    "Length": length[protocol],
                    "Count": number[protocol],
                    "Traffic": traffic[protocol]
                },
                "time":ttt
            }
        ]

        client.write_points(json_body, time_precision='n')

timer = RepeatTimer(1, dummyfn)
timer.start()
time.sleep(5)
timer.cancel()

        