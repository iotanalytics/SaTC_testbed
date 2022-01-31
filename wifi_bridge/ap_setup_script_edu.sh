#!/bin/bash


if [[ $# -lt 4 ]]
   then
     echo 'Usage: sudo ./ap_setup_script_edu.sh edu_wifi_ssid edu_wifi_identity edu_wifi_password hotspot_username hotspot_password'
     echo 'Usage: sudo ./ap_setup_script_edu.sh PAWS-Secure XXXXXXX XXXXXX sensorweb sensorweb128'
   exit 1
fi

wifi_username=$1
wifi_identity=$2
wifi_password=$3
hotspot_username=$4
hotspot_password=$5

echo 'WiFi SSID is '$wifi_username
echo 'WiFi Identity is'$wifi_identity
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
git pull 
make install
cd -

echo '#################################'
echo 'Setting..'

output=/etc/wpa_supplicant/wpa_supplicant.conf

echo "network={" >> $output
echo "    ssid=\"$wifi_username\"" >> $output
echo "    eap=PEAP" >> $output
echo "    key_mgmt=WPA-EAP" >> $output
echo "    phase2=\"auth=MSCHAPV2\"" >> $output
echo "    identity=\"$wifi_identity\"" >> $output
echo "    password=\"$wifi_password\"" >> $output
echo "}" >> $output

cat $output

automatic_local_file=/etc/rc.local

sed -i '$d' $automatic_local_file # delete the last valid line 'exit 0'

echo 'sudo ifconfig wlan0 down' >> $automatic_local_file # shutdown the pi's own wifi adaptor. then wlan1 will automatically connect to the Paw_secure
echo 'sudo ifconfig wlan2 down' >> $automatic_local_file
echo 'sudo create_ap wlan2 eth0' $hotspot_username $hotspot_password >> $automatic_local_file
echo "sudo /etc/init.d/ssh restart" >> $automatic_local_file
echo "exit 0" >> $automatic_local_file 

cat $automatic_local_file


echo 'Done!'
