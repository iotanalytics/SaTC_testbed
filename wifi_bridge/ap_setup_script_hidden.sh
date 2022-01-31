#!/bin/bash


if [[ $# -lt 4 ]]
   then
     echo 'Usage: sudo ./ap_setup_script_hidden.sh wifi_username wifi_password hotspot_username hotspot_password'
     echo 'Usage: sudo ./ap_setup_script_hidden.sh Existing_wifi Existing_wifi_password SensorwebWifi sensorweb'

   exit 1
fi

wifi_username=$1
wifi_password=$2
hotspot_username=$3
hotspot_password=$4

echo 'WiFi Username is '$wifi_username
echo 'WiFi Password is '$wifi_password
echo 'Hotspot Username is '$hotspot_username
echo 'Hotspot Password is '$hotspot_password




echo '#################################'
echo 'Installing Environment'
apt-get install git -y
apt-get install util-linux procps hostapd iproute2 iw haveged dnsmasq -y
apt-get install iptables -y

echo '#################################'
echo 'Installing create_ap'
git clone https://github.com/oblique/create_ap
cd create_ap
make install
cd -

echo '#################################'
echo 'Setting..'

output=/etc/wpa_supplicant/wpa_supplicant.conf

echo "network={" >> $output
echo "    ssid='$wifi_username'" >> $output
echo "    password='$wifi_password'" >> $output
echo "    key_mgmt=WPA-PSK" >> $output
echo "}" >> $output

cat $output

automatic_local_file=/etc/rc.local

sed -i '$d' $automatic_local_file

echo 'sudo create_ap wlan1 eth0' $hotspot_username $hotspot_password >> $automatic_local_file
echo "sudo /etc/init.d/ssh restart" >> $automatic_local_file
echo "exit 0" >> $automatic_local_file 

cat $automatic_local_file


echo 'Done!'