# demo uart transmit and receive


import time
from bluetooth import ble

import util
from bleuartlib import BleUartDevice


def addBleUartDevice(address, name):
    bleUartDevice = BleUartDevice(address)
    bleUartDevice.connect()
    bleUartDevice.enable_uart_receive(bleUartReceiveCallback)

    bleUartDevices.append({'device': bleUartDevice, 'name': name})


def bleUartReceiveCallback(data):
    print('Received data = {}'.format(data))


def sendCommandToAllBleUartDevices(command):
    for bled in bleUartDevices:
        bled['device'].send(command)


def disconnectFromAllBleUartDevices():
    for bled in bleUartDevices:
        bled['device'].disconnect()
        bled['device'] = None


try:

    bleUartDevices = []

    service = ble.DiscoveryService()
    devices = service.discover(2)

    print('********** Initiating device discovery......')

    for address, name in devices.items():

        if address == 'CF:BE:9E:5F:65:DA':

            print('Found BBC micro:bit [vavet]: {}'.format(address))
            addBleUartDevice(address, 'vavet')

            print('Added micro:bit device...')

        elif address == 'C8:06:B1:B4:66:53':

            print('Found BBC micro:bit [tipov]: {}'.format(address))
            addBleUartDevice(address, 'tipov')

            print('Added micro:bit device...')

        elif address == 'DF:60:7F:9B:61:F6':

            print('Found BBC micro:bit [popap]: {}'.format(address))
            addBleUartDevice(address, 'popap')

            print('Added micro:bit device...')

    if len(bleUartDevices) > 0:

        while True:

            response = input('Do you want to transmit command to micro:bit (Y/n) = ')

            if response == 'Y':
                command = input('Enter command to send = ')
                sendCommandToAllBleUartDevices(command)
                print('Finished sending command to all micro:bit devices...')

            time.sleep(0.1)

except KeyboardInterrupt:

    print('********** END')

except:

    print('********** UNKNOWN ERROR')

finally:

    disconnectFromAllBleUartDevices()
    print('Disconnected from all micro:bit devices')
