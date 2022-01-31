import datetime, time
import pytz
import json
import requests
import threading
from influxdb import InfluxDBClient
import warnings
warnings.filterwarnings("ignore")

def readData(data_array, start_time):
    # data array, start timestamp from Labviewer
    value_list = data_array
    start_time = start_time

    time_format = "%Y-%m-%d %H:%M:%S"
    tz_NY = pytz.timezone('America/New_York')
    currentTime = datetime.datetime.now(tz_NY)

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

    writeData = []
    # ts = datetime.datetime.strptime(start_time, time_format)
    # ts = tz_NY.localize(ts)
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