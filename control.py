# -*- coding: utf-8 -*-
# Code has been modified by Roc

from time import sleep
import sys
import random
import cloud4rpi
import ds18b20
import rpi
import RPi.GPIO as GPIO  # pylint: disable=F0401

# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = '8H9Kq4geUKccjazZaAMHA3rtr'

# Constants
LED_PIN = 12

# Change these values depending on your requirements.
DATA_SENDING_INTERVAL = 120  # secs
DIAG_SENDING_INTERVAL = 650  # secs
POLL_INTERVAL = 0.5  # 500 ms

LOCATIONS = [
    {'lat': 42.3149, 'lng': -83.0364}  # Roc's address
]

# Configure GPIO library
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)


# Handler for the button or switch variable
def led_control(value=None):
    GPIO.output(LED_PIN, value)
    return GPIO.input(LED_PIN)

# Define a function to get last reading of livingroom sensor(here using 4004918 as example, change as needed.)
def get_livingroom_sen():
    data = open("/home/pi/sensor.log", "r")
    sensor_id = '4004918'
    lines = data.readlines()
    last_lines = lines[-10:]
    last_lines= ' '.join([str(elem) for elem in last_lines])
    sensor_index = last_lines.rindex(sensor_id)
    sensor_id = last_lines[sensor_index:sensor_index+8]
    sensor_battery = last_lines[sensor_index+24:sensor_index+27]
    sensor_PIR1 = last_lines[sensor_index+30:sensor_index+32]
    sensor_PIR2 = last_lines[sensor_index+32:sensor_index+34]
    sensor_ambient = last_lines[sensor_index+34:sensor_index+38]
    sensor_ambient = str(int(sensor_ambient, 16)/32)
    sensor_IRtemp = last_lines[sensor_index+38:sensor_index+42]
    sensor_IRtemp = str(int(sensor_IRtemp, 16)/32)
    return [sensor_battery, sensor_PIR1, sensor_PIR2, sensor_ambient, sensor_IRtemp] 
# retrieve all sensor values, battery, ambient temerature, IR temperature, PIR1, PIR2
def get_livingroom_battery():
    return float(get_livingroom_sen()[0])/100

def get_livingroom_pir1():
    return int(get_livingroom_sen()[1],16)

def get_livingroom_pir2():
    return int(get_livingroom_sen()[2],16)

def get_livingroom_amb():
    return float(get_livingroom_sen()[3])

def get_livingroom_ir():
    return float(get_livingroom_sen()[4])
# Define a function to get last reading of bedroom sensor(here using 4000127 as example, change as needed.)
def get_bedroom_sen():
    data = open("/home/pi/sensor.log", "r")
    sensor_id = '4000127'
    lines = data.readlines()
    last_lines = lines[-10:]
    last_lines= ' '.join([str(elem) for elem in last_lines])
    sensor_index = last_lines.rindex(sensor_id)
    sensor_id = last_lines[sensor_index:sensor_index+8]
    sensor_battery = last_lines[sensor_index+24:sensor_index+27]
    sensor_PIR1 = last_lines[sensor_index+30:sensor_index+32]
    sensor_PIR2 = last_lines[sensor_index+32:sensor_index+34]  
    sensor_ambient = last_lines[sensor_index+34:sensor_index+38]
    sensor_ambient = str(int(sensor_ambient, 16)/32)
    sensor_IRtemp = last_lines[sensor_index+38:sensor_index+42]
    sensor_IRtemp = str(int(sensor_IRtemp, 16)/32)
    return [sensor_battery, sensor_PIR1, sensor_PIR2, sensor_ambient, sensor_IRtemp] 
    return

# retrieve all sensor values, battery, ambient temerature, IR temperature, PIR1, PIR2
def get_bedroom_battery():
    return float(get_bedroom_sen()[0])/100

def get_bedroom_pir1():
    return int(get_bedroom_sen()[1],16)

def get_bedroom_pir2():
    return int(get_bedroom_sen()[2],16)

def get_bedroom_amb():
    return float(get_bedroom_sen()[3])

def get_bedroom_ir():
    return float(get_bedroom_sen()[4])

def listen_for_events():
    # Write your own logic here
    result = random.randint(1, 5)
    if result == 1:
        return 'RING'

    if result == 5:
        return 'BOOM'

    return 'IDLE'


def get_location():
    return random.choice(LOCATIONS)


def sensor_not_connected():
    return 'Sensor not connected'


def main():
    # Load w1 modules
    #ds18b20.init_w1()

    # Detect ds18b20 temperature sensors
    #ds_sensors = ds18b20.DS18b20.find_all()

    # Put variable declarations here
    # Available types: 'bool', 'numeric', 'string', 'location'
    variables = {
        #'Room Temp': {
        #    'type': 'numeric' if ds_sensors else 'string',
        #    'bind': ds_sensors[0] if ds_sensors else sensor_not_connected
        #},
        # 'Outside Temp': {
        #     'type': 'numeric' if ds_sensors else 'string',
        #     'bind': ds_sensors[1] if ds_sensors else get_empty_value
        # },
        'BedSenBattery': {
            'type': 'numeric',
            'bind': get_bedroom_sen()[0]
        },
        'LED On': {
            'type': 'bool',
            'value': False,
            'bind': led_control
        },
        'CPU Temp': {
            'type': 'numeric',
            'bind': rpi.cpu_temp
        },
        'STATUS': {
            'type': 'string',
            'bind': listen_for_events
        },
        'Location': {
            'type': 'location',
            'bind': get_location
        },
        'LivingroomAmb': {
            'type': 'numeric',
            'bind': get_livingroom_amb
        },
        'BedroomAmb': {
            'type': 'numeric',
            'bind': get_bedroom_amb
        },
        'LivingroomBattery': {
            'type': 'numeric',
            'bind': get_livingroom_battery
        },
        'BedroomBattery': {
            'type': 'numeric',
            'bind': get_bedroom_battery
        },
        'LivingroomPIR1': {
            'type': 'numeric',
            'bind': get_livingroom_pir1
        },
        'BedroomPIR1': {
            'type': 'numeric',
            'bind': get_bedroom_pir1
        },
        'LivingroomPIR2': {
            'type': 'numeric',
            'bind': get_livingroom_pir2
        },
        'BedroomPIR2': {
            'type': 'numeric',
            'bind': get_bedroom_pir2
        },
        'LivingroomIR': {
            'type': 'numeric',
            'bind': get_livingroom_ir   
        },
        'BedroomIR': {
            'type': 'numeric',
            'bind': get_bedroom_ir 
        }
    }

    diagnostics = {
        'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name,
        'Client Version:': cloud4rpi.__version__,
        'BedAmb': get_livingroom_amb
    }
    device = cloud4rpi.connect(DEVICE_TOKEN)

    # Use the following 'device' declaration
    # to enable the MQTT traffic encryption (TLS).
    #
    # tls = {
    #     'ca_certs': '/etc/ssl/certs/ca-certificates.crt'
    # }
    # device = cloud4rpi.connect(DEVICE_TOKEN, tls_config=tls)

    try:
        device.declare(variables)
        device.declare_diag(diagnostics)

        device.publish_config()

        # Adds a 1 second delay to ensure device variables are created
        sleep(1)

        data_timer = 0
        diag_timer = 0

        while True:
            if data_timer <= 0:
                device.publish_data()
                data_timer = DATA_SENDING_INTERVAL

            if diag_timer <= 0:
                device.publish_diag()
                diag_timer = DIAG_SENDING_INTERVAL

            sleep(POLL_INTERVAL)
            diag_timer -= POLL_INTERVAL
            data_timer -= POLL_INTERVAL

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.exception("ERROR! %s %s", error, sys.exc_info()[0])

    finally:
        sys.exit(0)


if __name__ == '__main__':
    main()
