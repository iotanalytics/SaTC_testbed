from influxdb import InfluxDBClient
import time, datetime
import pytz
import pandas as pd

host = "sensorweb.us"
username = "test"
port = 8086
pwd = "sensorweb"
dbName = "testdb"
measurement = "NI_Waveform"
location = "bowenRoom"
isSSL = True
client = InfluxDBClient(
    host=host, port=port, username=username, password=pwd, database=dbName, ssl=isSSL
)

time_format = "%Y-%m-%d %H:%M:%S"
tz_NY = pytz.timezone("America/New_York")

# define the reading time range of datebase
start_time = datetime.datetime(2021, 3, 2, 20, 46, 30)
end_time = datetime.datetime(2021, 3, 2, 20, 55, 00)

start_timestamp = start_time.timestamp() * 1000
start_str = str(int((start_timestamp) * 1000000))

end_timestamp = end_time.timestamp() * 1000
end_str = str(int((end_timestamp) * 1000000))

readQuery = (
    "SELECT * FROM "
    + measurement
    + " WHERE time > "
    + start_str
    + " and time < "
    + end_str
)

result = client.query(readQuery)
values = result.get_points()
time_col = []
channel_1 = []
channel_2 = []
channel_3 = []

for point in values:
    time_col.append(point["time"])
    channel_1.append(point["channel_1"])
    channel_2.append(point["channel_2"])
    channel_3.append(point["channel_3"])

lists = [time_col, channel_1, channel_2, channel_3]
df = pd.DataFrame(lists).T

df.to_csv("output.csv", index=False, sep=",")