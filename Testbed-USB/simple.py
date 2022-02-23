# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:03:23 2021

@author: sjc48278
"""
from queue import Queue
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

machine_url = '127.0.0.1'
service_protocol = 'ws://'
service_port = '8090'
service_url = service_protocol + machine_url + ':' + service_port
  
q=Queue()

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




def getConnection():
    #Note on USB IDs
    #Vendor ID:	  1357	P&E Microcomputer Systems
    #Device ID:   0089	OpenSDA - CDC Serial Port
    #Looking for "DEVICE ID 1357:0089" using find_class
    venId = 0x1357
    devId = 0x0089
    os.environ['PYUSB_DEBUG'] = 'debug'
    usb.core.find()
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    if ports != False:
        cp = 'COM9'
        connection = 'RS232;port='+ cp +';speed=115200;tmoRI=40;tmoRTM=40;tmoRTC=50;tmoWTM=40;tmoWTC=50;'
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

    ws = await websockets.connect(service_url)
    jrpc = WebSocketsClient(ws)


    connection = getConnection()
    if connection != '':
        await SendRequest(jrpc, 'StartComm', connection)
        await SendRequest(jrpc, 'DefineVariable', appOnOff)
        await SendRequest(jrpc, 'DefineVariable', speedRequired)
        await SendRequest(jrpc, 'DefineVariable', Mode)
        await SendRequest(jrpc, 'DefineVariable', clearFaults)
        
        data = await SendRequest(jrpc, 'ReadVariable', 'On/Off')
        if data != 0 :
            await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
            await SendRequest(jrpc, 'WriteVariable', 'On/Off', 0)
            current_speed = await SendRequest(jrpc, 'ReadVariable', 'Speed Required')
            if current_speed != 80 :
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 0)
                await SendRequest(jrpc, 'WriteVariable', 'Speed Required', 80)
            print("motor stopped")
        else:
            print("motor board code is operational")
            #await SendRequest(jrpc, 'WriteVariable', 'On/Off', 0)
    else:
        exit(1)

    
    
#"""    
if __name__ == "__main__":
    asyncio.run(main()) 
#"""

