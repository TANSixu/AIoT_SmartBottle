# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('Water bottle!')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# import time
# from bluetooth import ble
#
# import util
# from bleuartlib import BleUartDevice
#
#
# def addBleUartDevice(address, name):
#     bleUartDevice = BleUartDevice(address)
#     bleUartDevice.connect()
#     bleUartDevice.enable_uart_receive(bleUartReceiveCallback)
#
#     bleUartDevices.append({'device': bleUartDevice, 'name': name})
#
#
# def bleUartReceiveCallback(data):
#     print('Received data = {}'.format(data))
#     # return data
#
# def sendCommandToAllBleUartDevices(command):
#     for bled in bleUartDevices:
#         bled['device'].send(command)
#
#
# def disconnectFromAllBleUartDevices():
#     for bled in bleUartDevices:
#         bled['device'].disconnect()
#         bled['device'] = None
#
#
# try:
#
#     bleUartDevices = []
#
#     service = ble.DiscoveryService()
#     devices = service.discover(2)
#
#     print('********** Initiating device discovery......')
#
#     for address, name in devices.items():
#
#         if address == 'CF:BE:9E:5F:65:DA':
#
#             print('Found BBC micro:bit [vavet]: {}'.format(address))
#             addBleUartDevice(address, 'vavet')
#
#             print('Added micro:bit device...')
#
#         elif address == 'C8:06:B1:B4:66:53':
#
#             print('Found BBC micro:bit [tipov]: {}'.format(address))
#             addBleUartDevice(address, 'tipov')
#
#             print('Added micro:bit device...')
#
#         elif address == 'DF:60:7F:9B:61:F6':
#
#             print('Found BBC micro:bit [popap]: {}'.format(address))
#             addBleUartDevice(address, 'popap')
#
#             print('Added micro:bit device...')
#
#     if len(bleUartDevices) > 0:
#
#         while True:
#
#             # data = bleUartDevices[0]['device'].enable_uart_receive(bleUartReceiveCallback)
#             response = input('Do you want to transmit command to micro:bit (Y/n) = ')
#
#             if response == 'Y':
#                 command = input('Enter command to send = ')
#                 sendCommandToAllBleUartDevices(command)
#                 print('Finished sending command to all micro:bit devices...')
#
#             time.sleep(0.1)
#
# except KeyboardInterrupt:
#
#     print('********** END')
#
# except:
#
#     print('********** UNKNOWN ERROR')
#
# finally:
#
#     disconnectFromAllBleUartDevices()
#     print('Disconnected from all micro:bit devices')

# demo uart receive


# import time
# from bluetooth import ble
#
# import util
# from bleuartlib import BleUartDevice
#
# try:
#
#     bleUartDevice1 = None
#     found_microbit = False
#
#     service = ble.DiscoveryService()
#     devices = service.discover(2)
#
#     print('********** Initiating device discovery......')
#
#     for address, name in devices.items():
#
#         found_microbit = False
#
#         if address == 'CF:BE:9E:5F:65:DA':
#             print('Found BBC micro:bit [vavet]: {}'.format(address))
#             found_microbit = True
#             break
#
#     if found_microbit:
#
#         bleUartDevice1 = BleUartDevice(address)
#         bleUartDevice1.connect()
#         print('Connected to micro:bit device')
#
#         while True:
#             temp = bleUartDevice1.readTemperature()
#             print('Temperature = {}'.format(temp))
#             time.sleep(0.1)
#
# except KeyboardInterrupt:
#
#     print('********** END')
#
# except Exception :
#     print(Exception.message)
#     print('********** UNKNOWN ERROR')
#
# finally:
#
#     if bleUartDevice1 != None:
#         bleUartDevice1.disconnect()
#         bleUartDevice1 = None
#         print('Disconnected from micro:bit device')
# demo temperature service


# import time
# from bluetooth import ble
#
# import util
# from bleuartlib import BleUartDevice
#
# try:
#
#     bleUartDevice1 = None
#     found_microbit = False
#
#     service = ble.DiscoveryService()
#     devices = service.discover(2)
#
#     print('********** Initiating device discovery......')
#
#     for address, name in devices.items():
#
#         found_microbit = False
#
#         if address == 'CF:BE:9E:5F:65:DA':
#             print('Found BBC micro:bit [vavet]: {}'.format(address))
#             found_microbit = True
#             break
#
#     if found_microbit:
#
#         bleUartDevice1 = BleUartDevice(address)
#         bleUartDevice1.connect()
#         print('Connected to micro:bit device')
#
#         while True:
#             accelerometer = bleUartDevice1.readAccelerometer()
#             print('Accelerometer = x={} y={} z={}'.format(accelerometer[0], accelerometer[1], accelerometer[2]))
#             time.sleep(1)
#
# except KeyboardInterrupt:
#
#     print('********** END')
#
# except Exception:
#
#     print('********** UNKNOWN ERROR')
#     print(Exception.message)
#
# finally:
#
#     if bleUartDevice1 != None:
#         bleUartDevice1.disconnect()
#         bleUartDevice1 = None
#         print('Disconnected from micro:bit device')

# import time
# from bluetooth import ble
#
# import util
# from bleuartlib import BleUartDevice
#
#
# def bleTemperatureReceiveCallback(data):
#     print('Received data = {}'.format(data))
#
#
# try:
#
#     bleUartDevice1 = None
#     found_microbit = False
#
#     service = ble.DiscoveryService()
#     devices = service.discover(2)
#
#     print('********** Initiating device discovery......')
#
#     for address, name in devices.items():
#
#         found_microbit = False
#
#         if address == 'CF:BE:9E:5F:65:DA':
#             print('Found BBC micro:bit [vavet]: {}'.format(address))
#             found_microbit = True
#             break
#
#     if found_microbit:
#
#         bleUartDevice1 = BleUartDevice(address)
#         bleUartDevice1.connect()
#         print('Connected to micro:bit device')
#
#         bleUartDevice1.enable_temperature_receive(bleTemperatureReceiveCallback)
#         print('Receiving data...')
#
#         while True:
#             time.sleep(0.1)
#
# except KeyboardInterrupt:
#
#     print('********** END')
#
# except Exception:
#
#     print('********** UNKNOWN ERROR')
#     print(Exception.message)
#
# finally:
#
#     if bleUartDevice1 != None:
#         # bleUartDevice1.disable_temperature_receive()
#         bleUartDevice1.disconnect()
#         bleUartDevice1 = None
#         print('Disconnected from micro:bit device')

import pygatt
import time
import struct
import matplotlib.pyplot as plt
import numpy as np
import sys
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.GATTToolBackend()
rx=[]
ry=[]
rz=[]

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    accelerometer = value

    x_bytes = bytes([accelerometer[0], accelerometer[1]])
    y_bytes = bytes([accelerometer[2], accelerometer[3]])
    z_bytes = bytes([accelerometer[4], accelerometer[5]])

    x_short = struct.unpack('<h', x_bytes)[0]
    y_short = struct.unpack('<h', y_bytes)[0]
    z_short = struct.unpack('<h', z_bytes)[0]


    plt.ion()
    
    rx.append(x_short)
    ry.append(y_short)
    rz.append(z_short)
    plt.clf()
    plt.plot(rx,label='x')
    plt.plot(ry, label='y')
    plt.plot(rz, label='z')
    plt.legend()
    plt.show()
    plt.pause(0.1)
    # sys.exit(0)
    print('Accelerometer = x={} y={} z={}'.format(x_short, y_short, z_short))


def temp_handle(handle, value):
    print(f'received: {value}')

try:
    adapter.start()
    device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
    print('found')
    time.sleep(15)
    # device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
    print('connected')
    # device.subscribe("e95d9250-251d-470a-a062-fa1922dfa9a8",callback=temp_handle)
    while True:
        num = device.char_read_handle('0x27')
        handle_data(handle='0x27', value=num)
        time.sleep(0.05)
   
finally:
    adapter.stop()