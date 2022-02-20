# Launch ssh attack to the raspberry pi mesh network
A program to launch the ssh stepstone attack to the raspberry Pi mesh network, which would affect the energy consumption of Pis. By analyzing those data, we could detect the potential vulnerabilities of Raspberry Pis.

We use **collectd** to collect those energy consumption data and push to the InfluxDB. Eventually using Grafana to visuliaze the data.
```grafanaPanel.json``` is the configuration file for Grafana. Import this JSON file would generate the same Grafana panel as below.

## Usage:
```bash
chmod a+x scan_attack.sh

# The arguments are the victims' IP addresses of the stepstone attack. The number is arbitrary.
./scan_attack.sh ip1 ip2 ip3 ip4
```

## Notes:
Before launching the attack, please make sure to save the public keys from different Pis into every Pi's known host file, which locates in the directory ```~/.ssh/known_hosts```.