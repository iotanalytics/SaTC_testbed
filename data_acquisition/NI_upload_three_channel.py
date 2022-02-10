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
from wavefrom_to_PMU import feature_extract

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
pwd = "sensorweb"
dbName = "testdb"
measurement = "NI_Waveform"
location = "sensorweb128"
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
    cmnd = conn.recv(6*2000*4*8)  # 6 channels * 2khz * 4bytes * 8bit
    data_array = json.loads(cmnd.decode())

    # value_list is uploaded to influxdb
    value_list = data_array
    value_list = df_int_to_float(value_list)
    value_list = value_list.to_numpy().transpose()

    features = feature_extract(value_list, f_s=5000)
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
                    "channel_0": value_list[0][i],
                    "channel_1": value_list[1][i],
                    "channel_2": value_list[2][i],
                    "channel_3": value_list[0][i],
                    "channel_4": value_list[1][i],
                    "channel_5": value_list[2][i],
                },
                "time": timestamp,
            }
        )
        # timestamp = timestamp + 1000000
        timestamp = timestamp + 5000000 # 0.0005 second
    client.write_points(
        writeData, time_precision="n", batch_size=10000, protocol="json"
    )
    value_list = []

server.close()