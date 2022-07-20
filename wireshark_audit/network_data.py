# Updated 
# ! stdbuf -i0 -oL -e0 tshark -i enp0s31f6 -q -T fields -e frame.time_relative -e _ws.col.Protocol -e eth.src -e eth.dst -e frame.len -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | python /home/sensorweb/Desktop/SaTC_testbed/wireshark_audit/network_data.py

# stdbuf -i0 -oL -e0 tshark -i enp0s31f6 -q -T fields -e frame.time_relative -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | python /home/sensorweb/Desktop/SaTC_testbed/wireshark_audit/network_data.py

import sys
from datetime import datetime
from threading import Timer
from influxdb import InfluxDBClient
isSSL = True
client = InfluxDBClient(host="sensorwebdata.engr.uga.edu", port=8086, username="test", password="sensorweb", ssl = isSSL)

currentTime = datetime.now()
timestamp = int(currentTime.timestamp()*1000000000)
_flag = True
import warnings
warnings.filterwarnings("ignore")

### start a timer here refer: https://github.com/SongClass/SimTCP 


class RepeatTimer(Timer):
   def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def wiresharkRawData(protocol, src_MAC_Address, dst_MAC_Address, src_ip, dst_ip, src_port, dst_port, ttt, length):
        client.switch_database("WiresharkRawData")
        json_body = [
            {
                "measurement": "WiresharkRawData",
                "tags": {
                    "Protocol":protocol,
                    "Source MAC": src_MAC_Address,
                    "Destination MAC": dst_MAC_Address,
                    "Source IP":src_ip,
                    "Destination IP":dst_ip,
                    "Source Port": src_port,
                    "Destination Port": dst_port
                },
                "fields":{
                    "Length": length
                },
                "time":ttt
            }

        ]
        client.write_points(json_body, time_precision='n')

def calcData(temp):
    print(" CalcData running after 5 seconds")
    global _flag
    client.switch_database('CalcData')
    for key, value in temp.items():
        json_body = [
            {
                "measurement": "CalcData",
                "tags": {
                    "Protocol":key
                },
                "fields":{
                    "Count": value[0],
                    "Traffic": value[1]
                }
            }

        ]       
        client.write_points(json_body, time_precision='n')
        
    _flag = True
            

def main():
    global _flag
    calcDict = {}
    for something in sys.stdin:
        packet = something.split()
        print(packet)
        time = int(float(packet[0]))
        protocol = str(packet[1])
        length = int(packet[2])
        if len(packet) == 9:
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = packet[5]
            dst_ip = packet[6]
            src_port = packet[7]
            dst_port = packet[8]
        elif len(packet) == 5 or protocol == 'ARP':
            src_MAC_Address = packet[2]
            dst_MAC_Address = packet[3]
            src_ip = "FFFFFF"
            dst_ip = "FFFFFF"
            src_port = 0
            dst_port = 0
        elif len(packet) == 7 and protocol == "IGMPv3":
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = packet[5]
            dst_ip = packet[6]
            src_port = 0
            dst_port = 0
        elif len(packet) < 9 and protocol == "MDNS":
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = "FFFFFF"
            dst_ip = "FFFFFF"
            src_port = packet[5]
            dst_port = packet[6]
        elif protocol == "ADwin" and len(packet) < 7:
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = "FFFFFF"
            dst_ip = "FFFFFF"
            src_port = 0
            dst_port = 0
        elif protocol == "NXP" and len(packet) == 11:
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = int(packet[6])
            dst_ip = int(packet[7])
            src_port = int(packet[8])
            dst_port = int(packet[9])
        else:
            src_MAC_Address = packet[3]
            dst_MAC_Address = packet[4]
            src_ip = "FFFFFF"
            dst_ip = "FFFFFF"
            src_port = 0
            dst_port = 0
        ttt = timestamp + int(round(time)*1000000000)

        if protocol in calcDict.keys():
            value = calcDict.get(protocol)[0]
            value1 = calcDict.get(protocol)[1]
            calcDict[protocol][0] = value + 1
            calcDict[protocol][1] = value1 + length
        else:
            calcDict.update({protocol:[1, length]})
        
        #wiresharkRawData(protocol, src_MAC_Address, dst_MAC_Address, src_ip, dst_ip, src_port, dst_port, ttt, length)
        if _flag:
            temp = calcDict.copy()
            calcDict.clear()
            t5 = Timer(5, calcData, [temp])
            t5.start()
            _flag = False
            
        
        #print("Success!")
     

if __name__ == '__main__':
    main()
    
        
