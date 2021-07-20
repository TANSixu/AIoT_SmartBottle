import pygatt
import time
import struct
import matplotlib.pyplot as plt
import sys
import logging
from extract_util import *
import numpy as np
from multiprocessing import Queue
from threading import Thread


adapter = pygatt.GATTToolBackend()
block_num = 100
start=0


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

    return x_short
    # print('Accelerometer = x={} y={} z={}'.format(x_short, y_short, z_short))


def get_data(mqtt):
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
            xv = handle_data(handle='0x27', value=num)
            mqtt.put(xv)
            # time.sleep(0.1)

    finally:
        adapter.stop()


def process_data(mqtt):
    x_data=[]
    while True:
        if len(x_data) < block_num:
            x_data.append(mqtt.get())
            continue

        x_pro = np.array(x_data)
        x_pro = low_pass_filter(x_pro, 6)
        valley = valley_detection(x_pro, 0.01, 3, 1.0)
        raw_event = threshold(x_pro, valley, 15, 1.0)
        for t in raw_event:
            feature = feature_extract(t)
            print(feature)
        x_data.clear()


if __name__ == '__main__':
    mqtt = Queue()                           #创建一个队列
    pro = Thread(target=get_data,args=(mqtt,))
    cus = Thread(target=process_data,args=(mqtt,))
    pro.start()
    cus.start()
