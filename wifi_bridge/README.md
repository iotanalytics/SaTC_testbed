# Pi Wifi Bridge setup

This program sets up a Raspberry Pi as a WiFi bridge that connects to Internet through WiFi infrastructure and provides WiFi AP to other devices. Steps to set up:

(1) Install a 32-bit Raspberry Pi image (2022-01-28 version) onto the SD card, seet up ssh and WiFi: https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup. If you use MacOS, you may just follow below:

```
touch /Volumes/boot/ssh
nano /Volumes/boot/wpa_supplicant.conf
```
In wpa_supplicant.conf, write
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```

(2) After wifi connected andd ssh login, plug in two USB WiFi dongle (https://www.amazon.com/Connecting-Wireless-Adapter-150Mbps-Raspberry/dp/B073J3HXZH/ref=sr_1_5?crid=OWY6FLNYBGR7&keywords=raspberry+pi+wifi+dongle&qid=1653574938&sprefix=raspberry+pi+wifi+dongle%2Caps%2C1087&sr=8-5) into Raspberry Pi.

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

### Reboot:
```
sudo reboot
```
