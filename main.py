import pygatt
import time
import struct
import matplotlib.pyplot as plt
import sys
import logging
import pandas as pd
import numpy as np

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

    print('Accelerometer = x={} y={} z={}'.format(x_short, y_short, z_short))

    if(len(rx)<500):
        rx.append(x_short)
        ry.append(y_short)
        rz.append(z_short)
    else:
        plt.plot(rx,label='x')
        # plt.plot(ry, label='y')
        # plt.plot(rz, label='z')
        # df=pd.DataFrame()
        xarr=np.array(rx)
        np.save('x_data.npy', xarr)
        plt.legend()
        plt.show()
        # plt.pause(0.1)
        # plt.ioff()
        sys.exit(0)



def temp_handle(handle, value):
    print(f'received: {value}')

try:
    adapter.start()
    device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
    print('found')
    time.sleep(15)
    # device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
    print('connected')
    # device.subscribe("e95dca4b-251d-470a-a062-fa1922dfa9a8",callback=handle_data)
    while True:
        num = device.char_read_handle('0x27')
        handle_data(handle='0x27', value=num)
        time.sleep(0.01)
   
finally:
    adapter.stop()