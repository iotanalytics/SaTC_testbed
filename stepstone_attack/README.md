# Launch ssh attack to the raspberry pi mesh network
A program to launch the ssh stepstone attack to the raspberry Pi mesh network, which would affect the energy consumption of Pis. We use collectd to collect those energy consumption data and push to the InfluxDB. Eventually using Grafana to visuliaze the data.
```grafanaPanel.json``` is the configue file for Grafana.

## Usage:
```
chmod a+x scan_attack.sh
./scan_attack.sh ip1 ip2 ip3 ip4
```