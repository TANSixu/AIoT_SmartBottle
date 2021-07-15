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
    # return data

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
            continue
            # data = bleUartDevices[0]['device'].enable_uart_receive(bleUartReceiveCallback)
            # response = input('Do you want to transmit command to micro:bit (Y/n) = ')
            #
            # if response == 'Y':
            #     command = input('Enter command to send = ')
            #     sendCommandToAllBleUartDevices(command)
            #     print('Finished sending command to all micro:bit devices...')
            #
            # time.sleep(0.1)

except KeyboardInterrupt:

    print('********** END')

except:

    print('********** UNKNOWN ERROR')

finally:

    disconnectFromAllBleUartDevices()
    print('Disconnected from all micro:bit devices')

# demo uart receive


# import time
# from bluetooth import ble
#
# import util
# from bleuartlib import BleUartDevice
#
#
# def bleUartReceiveCallback(data):
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
#         if address == 'E1:6E:8C:EC:C6:68':
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
#         data = bleUartDevice1.enable_uart_receive(bleUartReceiveCallback)
#         print('Receiving data...')
#
#         while True:
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
#     if bleUartDevice1 != None:
#         bleUartDevice1.disconnect()
#         bleUartDevice1 = None
#         print('Disconnected from micro:bit device')
