# Pi Wifi Bridge setup
This script turns a raspberry Pi into a wifi bridge.

## Usage:
```chmod a+x ap_setup_script.sh```
### edu WiFi:
```bash
sudo ./ap_setup_script.sh -edu edu_wifi_ssid edu_wifi_identity edu_wifi_password hotspot_username hotspot_password
```
e.g. ```sudo ./ap_setup_script.sh -edu PAWS-Secure XXXXXXX XXXXXX sensorweb sensorweb128```

### regular WiFi:
```bash
sudo ./ap_setup_script.sh wifi_username wifi_password hotspot_username hotspot_password
```
e.g. ```Usage: sudo ./ap_setup_script.sh Existing_wifi Existing_wifi_password SensorwebWifi sensorweb```