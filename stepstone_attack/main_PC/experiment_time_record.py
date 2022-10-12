from influxdb import InfluxDBClient
import sys, warnings
warnings.filterwarnings("ignore")

# influxDB config
host = "sensorwebdata.engr.uga.edu"

username = "test"
port = 8086
pwd = "sensorweb"
dbName = "experiment_time_log"
measurement = "log"
isSSL = True

client = InfluxDBClient(
    host=host, port=port, username=username, password=pwd, database=dbName, ssl=isSSL
)


def main():
    if len(sys.argv) <= 1:
        print("Example: " + sys.argv[0] + " start. For record the initial start timepoints of the experiment session.")
        sys.exit()

    if sys.argv[1] == "start":
        data_label = "experiment_start_time"
    elif sys.argv[1] == "end":
        data_label = "experiment_end_time"
    else:
        print("wrong argument: type start or end")
        sys.exit()
    

    writeData = [
        {
            "measurement": measurement,-ssl -unsafeSsl -host sensorwebdata.engr.uga.edu
            "tags": {"data_label": data_label},
            "fields":{
                "value":1,
            }
        }
    ]
    client.write_points(
        writeData, time_precision="s", batch_size=500, protocol="json"
    )



if __name__ == "__main__":
    main()

# How to transfer from influxdb to csv file
# This shows an example of export the thermal file from database to csv file.
# influx -ssl -unsafeSsl -host sensorwebdata.engr.uga.edu -database 'collectd_pi2' -execute "SELECT * from thermal_value where time >= '2022-06-02T00:00:00Z' AND time <= '2022-06-11T00:00:00Z'" -format csv > thermal_pi2.csv
