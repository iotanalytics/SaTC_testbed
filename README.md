# SaTC_testbed
This repo contains the SaTC project testbed setup related work.

## Data Acquisition
Folder **data_acquisition** contains the code for extracting the sensor data from motors and uploading to the InfluxDB. The specific data acquisition device is **NI cDAQ-9186**.

## Testbed-USB
This folder contains the script for setting up the motors hardware.

## Stepstone Attack
Folder **stepstone_attack** contains the code for launching the stepstone attack to penetrate the Raspberry pi then control the motor spinning.

## Wifi bridge
Folder **wifi_bridge** contains the code for turning a Raspberry Pi intor a wifi relay bridge in either education network (e.g. PAW-SECURE) or common wifi environment.