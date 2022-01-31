import socket
import json
import datetime, time
from typing import Sized
import pytz
import json
import requests
import threading
from influxdb import InfluxDBClient
import warnings
import pandas as pd

warnings.filterwarnings("ignore")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8089))
server.listen(1)


time_format = "%Y-%m-%d %H:%M:%S"
tz_NY = pytz.timezone("America/New_York")


# influxDB config
host = "sensorweb.us"
username = "test"
port = 8086
pwd = ""
dbName = "testdb"
measurement = "NI_Waveform"
location = "bowenRoom"
isSSL = True
client = InfluxDBClient(
    host=host, port=port, username=username, password=pwd, database=dbName, ssl=isSSL
)


def df_int_to_float(df):
    for i in range(len(df)):
        for j in range(len(df[i])):
            df[i][j] = float(df[i][j])
    return df


while True:
    conn, addr = server.accept()
    cmnd = conn.recv(81920)  # The default size of the command packet is 4 bytes
    data_array = json.loads(cmnd.decode())

    # value_list is uploaded to influxdb
    value_list = data_array
    print(len(value_list))
    # print(value_list)
    value_list = df_int_to_float(value_list)

    writeData = []
    # ts = datetime.datetime.strptime(start_time, time_format)
    # ts = tz_NY.localize(ts)
    currentTime = datetime.datetime.now(tz_NY)
    timestamp = int(currentTime.timestamp() * 1000000000)
    for i in range(len(value_list[0])):
        # timestamp = int(ts.timestamp() * 1000) # epoch time
        writeData.append(
            {
                "measurement": measurement,
                "tags": {"location": [location]},
                "fields": {
                    "channel_1": value_list[0][i],
                    "channel_2": value_list[1][i],
                    "channel_3": value_list[2][i],
                },
                "time": timestamp,
            }
        )
        timestamp = timestamp + 1000000
    client.write_points(
        writeData, time_precision="n", batch_size=10000, protocol="json"
    )
    value_list = []

server.close()