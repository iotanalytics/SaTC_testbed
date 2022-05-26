# Pi Wifi Bridge setup

This program sets up a Raspberry Pi as a WiFi bridge that connects to Internet through WiFi infrastructure and provides WiFi AP to other devices. Steps to set up:

(1) Install a 32-bit Raspberry Pi image (2022-01-28 version) onto the SD card, seet up ssh and WiFi: https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup;
(2) Plug in two USB WiFi dongle into Raspberry Pi - what WiFi modules have been used by us? Maybe any plugged and go USB WiFi dongle will do.
(3) Set up script to connect to infrastructure WiFi and open WiFi AP mode for others to connect. This is referred from: https://inrg.soe.ucsc.edu/howto-connect-raspberry-to-eduroam/

## Usage:
```chmod a+x ap_setup_script.sh```
### edu WiFi:
```bash
sudo ./ap_setup_script.sh -edu edu_wifi_ssid edu_wifi_identity edu_wifi_password hotspot_username hotspot_password
```
e.g. ```sudo ./ap_setup_script.sh -edu PAWS-Secure XXXXXXX XXXXXX sensorweb sensorweb128```

### regular WiFi:
```bash
sudo ./ap_setup_script.sh -wpa2 wifi_username wifi_password hotspot_username hotspot_password
```
e.g. ```Usage: sudo ./ap_setup_script.sh -wpa2 Existing_wifi Existing_wifi_password sensorweb sensorweb128```

### TODO:
```
echo 'sudo create_ap wlan2 eth0' $hotspot_username $hotspot_password >> $automatic_local_file
```
Here eth0 may need to be wlan1.
