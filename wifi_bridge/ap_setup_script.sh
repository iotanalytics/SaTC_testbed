#!/bin/bash


if [[ $# -lt 5 ]]
   then
     echo 'EDU wifi usage: sudo ./ap_setup_script.sh -edu edu_wifi_ssid edu_wifi_identity edu_wifi_password hotspot_username hotspot_password'
     echo 'Usage: sudo ./ap_setup_script.sh -edu PAWS-Secure engr-sensorweb SongLab@128 sensorweb sensorweb128'
     echo $'\n'
     echo 'Common wifi usage: sudo ./ap_setup_script.sh -wpa2 wifi_username wifi_password hotspot_username hotspot_password'
     echo 'Usage: sudo ./ap_setup_script.sh -wpa2 Existing_wifi Existing_wifi_password sensorweb sensorweb128'
   exit 1
fi

echo $1
echo $2
echo $3
echo $4
echo $'\n'

if [ "$1" == "-edu" ]; then
  echo "edu wifi mode:"
  wifi_username=$2
  wifi_identity=$3
  wifi_password=$4
  hotspot_username=$5
  hotspot_password=$6
else
  echo "hidden wifi mode:"
  wifi_username=$2
  wifi_password=$3
  hotspot_username=$4
  hotspot_password=$5
fi


echo '#################################'
echo 'Installing Environment'
apt-get install git -y
apt-get install util-linux procps hostapd iproute2 iw haveged dnsmasq -y
apt-get install iptables -y


echo '#################################'
echo 'Installing create_ap'
if [ ! -d "create_ap" ]; then
  echo "create_ap doesn't exist. Downloading..."
  git clone https://github.com/oblique/create_ap
else
  echo "create_ap folder already existed."
fi 

cd create_ap
git pull 
make install
cd -

echo '#################################'
echo 'Setting..'

output=/etc/wpa_supplicant/wpa_supplicant.conf

echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" > $output
echo "update_config=1" >> $output
echo "country=US" >> $output
echo "" >> $output

if [ "$1" == "-edu" ]; then
  echo "network={" >> $output
  echo "    ssid=\"$wifi_username\"" >> $output
  echo "    eap=PEAP" >> $output
  echo "    key_mgmt=WPA-EAP" >> $output
  echo "    phase2=\"auth=MSCHAPV2\"" >> $output
  echo "    identity=\"$wifi_identity\"" >> $output
  echo "    password=\"$wifi_password\"" >> $output
  echo "}" >> $output
else 
  echo "network={" >> $output
  echo "    ssid=\"$wifi_username\"" >> $output
  echo "    psk=\"$wifi_password\"" >> $output
  echo "    key_mgmt=WPA-PSK" >> $output
  echo "}" >> $output
fi

automatic_local_file=/etc/rc.local

sed -i '20, $d' $automatic_local_file # delete the lines from line 20

echo 'sudo ifconfig wlan0 down' >> $automatic_local_file # shutdown the pi's own wifi adaptor. then wlan1 will automatically connect to the Paw_secure
echo 'sudo ifconfig wlan2 down' >> $automatic_local_file
echo 'sudo create_ap wlan2 eth0' $hotspot_username $hotspot_password >> $automatic_local_file
echo "sudo /etc/init.d/ssh restart" >> $automatic_local_file
echo "exit 0" >> $automatic_local_file 


echo 'Done!'
