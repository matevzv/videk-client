#!/usr/bin/env python3

import re
import sys
import json
import time
import socket
import subprocess
import netifaces as ni
from datetime import datetime
from videkrestclient import Videk

lat = 46.042767
lon = 14.487632

def getserial():
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
 
    return cpuserial

conf = {}
with open('conf') as confile:
    for line in confile:
        name, var = line.partition("=")[::2]
        conf[name.strip()] = var.strip()

videk_api_key = conf['key']
videk = Videk(conf['api'], videk_api_key)

current_ip = None

if conf['id'] == "rpi-serial":
    machine_id = getserial()
else:
    machine_id = open('/etc/machine-id').readline().strip()

if videk.serverOnline():
    print("Videk server is online ...")
else:
    print("Videk server is offline ...")
    sys.exit(1)

def uploadSensors(node, node_id, sensor_type, sensors):
    for sensor in sensors:        
        sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])
        if sensor_id == None:
            videk.createSensor(node_id, sensor_type, sensor['name'],
                sensor['unit'])
            sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])

        measurement = '''{"latitude":"","longitude":"","ts":"","value":""}'''
        v = sensor['value']
        preparedData = []
        data = json.loads(measurement)
        data['value'] = v
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = lat
        data['longitude'] = lon
        preparedData.append(data)

        videk.uploadMesurements(preparedData, node_id, sensor_id)

def readSensors():
    sensors = []

    try:
        with open('sensors') as sensor_file:
            for line in sensor_file:
                sensor = {}
                name, var = line.partition("=")[::2]

                sensor['name'] = name.strip()
                sensor['value'] = round(float(var.strip()), 2)

                if 'temperature' in name:
                    sensor['unit'] = "C"
                elif 'battery' in name:
                    sensor['unit'] = "%"
                elif 'luminance' in name:
                    sensor['unit'] = "lm"
                elif 'position' in name:
                    sensor['unit'] = "G"
                
                sensors.append(sensor)
    except:
        pass

    return sensors

def writeLeds(extra_fields):
    for el in extra_fields:
        try:
            leds = el['LEDs']
            f = open("/tmp/ebottle/leds", "w")
            f.write(leds + "\n")
            f.close()
        except:
            pass

while True:

    node_model = videk.getNodeByHardwareId(machine_id)
    node_name = node_model['name']
    node_id = int(node_model['id'])

    #writeLeds(node_model['extra_fields'])
    
    s = readSensors()
    
    uploadSensors(node_name, node_id, "ebottle", s)

    time.sleep(10)
