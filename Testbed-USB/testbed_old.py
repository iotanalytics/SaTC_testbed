# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:03:23 2021

@author: sjc48278
"""
from datetime import datetime
import usb.core
import usb.util
import usb.backend.libusb1
import paho.mqtt.client as mqtt
import sys, os
import asyncio

import socket as s
import time
import subprocess
import datetime
import serial
import serial.tools.list_ports

import websockets
from jsonrpcclient.clients.websockets_client import WebSocketsClient

from pathlib import Path

channel = sys.argv[1]

global variable
appOnOff = {
    "name": "On/Off",
    "addr": "cntrState.usrControl.switchAppOnOff",
    "size": 1,
    "type": "uint"
    }

global variable
speedRequired = {
    "name": "Speed Required", 
    "addr": "drvFOC.pospeControl.wRotElReq", 
    "size": 4, 
    "type": "float"
    }
 
global variable
Mode = {
      "name": "Mode",
      "addr": "cntrState.usrControl.controlMode",
      "size": 1,
      "type": "uint"
    }

global variable
clearFaults =  {
      "name": "Clear Faults",
      "addr": "cntrState.usrControl.switchFaultClear",
      "size": 1,
      "type": "uint"
    }

def getConnection(channel):
    #Note on USB IDs
    #Vendor ID:	  1357	P&E Microcomputer Systems
    #Device ID:   0089	OpenSDA - CDC Serial Port
    #Looking for "DEVICE ID 1357:0089" using find_class
    venId = 0x1357
    devId = 0x0089
    os.environ['PYUSB_DEBUG'] = 'debug'
    usb.core.find()
    #print([comport.device for comport in serial.tools.list_ports.comports()])
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print("ports = ", ports)
    # USB serial port '/dev/ttyACM0'
    if ports != False:
        if str(ports[0]) != 'COM1' and str(ports[0]) != 'COM2':
            cp = str(ports[0])
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        elif str(ports[1]) != 'COM1' and str(ports[1]) != 'COM2':
            cp = str(ports[1])
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        else:
            cp = str(ports[2])
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        """
        if channel == '1':
            cp = 'COM9'
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        elif channel == '2':
            cp = 'COM8'
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        elif channel == '3':
            cp = 'COM7'
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        elif channel == '4':
            cp = 'COM6'
            connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
        else:
            connection = ''
        #"""
    else:
        print("Motorboard is not connected")
        connection =''
    return connection


async def SendRequest(jrpc, method, *args):
    response = await jrpc.request(method, *args)
    if response.data.result['success']:
        return response.data.result['data']
    else:
        raise Exception(response.data.result['error'])

    
async def main():
    p = Path('.')

    print("Channel is ",channel)

    machine_url = '127.0.0.1'
    service_protocol = 'ws://'
    service_port = '8090'
    service_url = service_protocol + machine_url + ':' + service_port

    ws = await websockets.connect(service_url)
    jrpc = WebSocketsClient(ws)
  
    speed_step = 20 # radians per second

    # create command file
    file_name = "motor_command"+channel+".txt"
    command_file = p / file_name
    if command_file.is_file() == False:
        f = open(file_name, "x")
        f.close()
    last_modification = command_file.stat().st_mtime

    m_file = "file"+channel

    # Connect to nxp server
    connection = getConnection(channel)
    print("connection = ", connection)
    #connection = 'RS232;port=COM8;speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'

    # Set motor board to default settings
    if connection != '':
        await SendRequest(jrpc, 'StartComm', connection)
        await SendRequest(jrpc, 'DefineVariable', appOnOff)
        await SendRequest(jrpc, 'DefineVariable', speedRequired)
        await SendRequest(jrpc, 'DefineVariable', Mode)
        await SendRequest(jrpc, 'DefineVariable', clearFaults)
        
        data = await SendRequest(jrpc, 'ReadVariable', 'On/Off')
        if data != 1 :
            await SendRequest(jrpc, 'WriteVariable', 'Clear Faults', 1)
            await SendRequest(jrpc, 'WriteVariable', 'On/Off', 1)
            current_speed = await SendRequest(jrpc, 'ReadVariable', 'Speed Required')
            if current_speed != 80 :
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 80)
            print("Program Started")
        else:
            print("motor board code is operational")
    else:
        exit(1)

    
    motor_command = ''
    # Loop to check for motor board commands from subscriber.py
    while motor_command != '6':
        time.sleep(2)
        file_modification = command_file.stat().st_mtime
        if  file_modification > last_modification:
            last_modification = file_modification
            # get first character from file            
 
            locals()[m_file] = open(file_name, "r")
            for line in locals()[m_file].readlines(): 
	            motor_command = line[0] 
	            break
            locals()[m_file].close()
            """
            with open(file_name) as f1:
                if channel == '1':                
                    motor_command = f1.readline()
                    f1.close()
                else:
                    print("Incorrect channel number was enter.  Program exiting.")
                    exit(1)
            #"""
            # Command Logic
            if motor_command == '0': # Stop Motor
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
            elif motor_command == '1': # Speed Up Motor in current rotating direction
                current_speed = await  SendRequest(jrpc, 'ReadVariable', 'Speed Required')
                if current_speed >= 0 and current_speed < (80-speed_step):
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 80)
                elif current_speed >= (80-speed_step):
                    if (current_speed + speed_step) < 314: # to prevent operating in the red
                        current_speed = current_speed + speed_step
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', current_speed)
                elif current_speed < 0 and current_speed > (-80 + speed_step):
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', -80)
                elif current_speed <= (-80 + speed_step):
                    if (current_speed - speed_step) > -314:
                        current_speed = current_speed - speed_step
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', current_speed) 
            elif motor_command == '2': # Slow Down Motor in current rotating direction
                current_speed = await  SendRequest(jrpc, 'ReadVariable', 'Speed Required')
                if current_speed >= (80 + speed_step):
                    if (current_speed - speed_step) >= 80:
                        current_speed = current_speed - speed_step
                        await SendRequest(jrpc, 'WriteVariable', 'Speed Required', current_speed)
                    elif current_speed >=0 and current_speed < 80:
                        await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
                elif (current_speed + speed_step) <= -60:                
                    current_speed = current_speed + speed_step
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', current_speed) 
                else:  
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
            elif motor_command == '3': # Stop Program
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
                await SendRequest(jrpc, 'WriteVariable', 'On/Off', 0)
                await SendRequest(jrpc, 'WriteVariable', 'Clear Faults', 1)
            elif motor_command == '4': # Clear Faults
                await SendRequest(jrpc, 'WriteVariable', 'Clear Faults', 1)
            elif motor_command == '5': # Restart Program
                #await SendRequest(jrpc, 'StartComm', connection)
                await SendRequest(jrpc, 'WriteVariable', 'Clear Faults', 1)
                await SendRequest(jrpc, 'WriteVariable', 'On/Off', 1)
                current_speed = await SendRequest(jrpc, 'ReadVariable', 'Speed Required')
                if current_speed != 80 :
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
                    await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 80)
            elif motor_command == '6': # Close COM port
                await SendRequest(jrpc, 'StopComm')
            elif motor_command == '':
                motor_command = ''
                # Do nothing
            else:
                print("An invalid command was entered")
    #"""

 
    
#"""    
if __name__ == "__main__":
    asyncio.run(main()) 
#"""

