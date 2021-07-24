import logging
from extract_util import *
import numpy as np
import struct
import time
import pygatt
import os
import matplotlib.pyplot as plt

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

    return x_short, y_short, z_short
    # print('Accelerometer = x={} y={} z={}'.format(x_short, y_short, z_short))


def get_data(mqtt):
    adapter = pygatt.GATTToolBackend()
    logging.basicConfig()
    logging.getLogger('pygatt').setLevel(logging.DEBUG)
    magic = 'Hello Smart Bottle!'
    wait = 15
    try:
        adapter.start()
        device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
        print('found')

        print(magic, 'Loading', end='')
        for i in range(wait):
            print('.', end=' ')
            time.sleep(1)
        print('\n')
        print('connected')
        start = time.time()
        while True:
            num = device.char_read_handle('0x27')
            xyz = handle_data(handle='0x27', value=num)
            mqtt.put(xyz)
            # time.sleep(0.1)

    finally:
        adapter.stop()


def process_data(mqtt, block_num):
    x_data=[]
    y_data=[]
    z_data=[]
    cnt=0
    while True:
        print(cnt)
        if len(x_data) < block_num:
            t_xyz = mqtt.get()
            x_data.append(t_xyz[0])
            y_data.append(t_xyz[1])
            z_data.append(t_xyz[2])
            cnt+=1
            continue

        x_pro = np.array(x_data)
        y_pro = np.array(y_data)
        z_pro = np.array(z_data)

        # plt.plot(x_pro, label='x')
        # plt.plot(y_pro, label='y')
        # plt.plot(z_pro, label='z')
        # plt.legend()
        # plt.show()

        my_data = np.array([x_pro, y_pro, z_pro])

        # only for test
        np.save('new_new_dataset1.npy', my_data)
        os._exit(1)

        x_pro = low_pass_filter(x_pro, 6)
        valley = valley_detection(x_pro, 0.01, 3, 1.0)
        raw_event = threshold(x_pro, valley, 15, 1.0)
        for t in raw_event:
            feature = feature_extract(t)
            print(feature)
        x_data.clear()