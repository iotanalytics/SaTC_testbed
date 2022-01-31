import socket
import json
import datetime, time
import pytz
import json
import requests
import threading
from influxdb import InfluxDBClient
import warnings
warnings.filterwarnings("ignore")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8089))
server.listen(1)


time_format = "%Y-%m-%d %H:%M:%S"
tz_NY = pytz.timezone('America/New_York')


# influxDB config
host = "sensorweb.us"
username = "test"
port = 8086
pwd = "sensorweb"
dbName = "testdb"
measurement = "NI_Waveform"
location = "bowenRoom"
isSSL = True
client = InfluxDBClient(host=host, port=port, username=username, password=pwd, database=dbName, ssl=isSSL)

def df_int_to_float(df):
    for i in range(len(df)):
        df[i] = float(df[i])
    return df

while True:
    conn, addr = server.accept()
    cmnd = conn.recv(1024)  # The default size of the command packet is 4 bytes
    try:
        data_array = json.loads(cmnd.decode())
    except:
        print("data_array")
    value_list = data_array
    value_list = df_int_to_float(value_list)

    writeData = []
    currentTime = datetime.datetime.now(tz_NY)
    timestamp = int(currentTime.timestamp() * 1000000000)
    for data_point in value_list:
        writeData.append(
            {
                "measurement": measurement,
                "tags":{
                    "location":location
                },
                "fields":{
                    "value": data_point
                },
                "time": timestamp
            }
        )
        timestamp = timestamp + 5000000
    client.write_points(writeData, time_precision='n', batch_size=10000, protocol='json')

server.close()