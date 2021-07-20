import pygatt
import time
import struct
import matplotlib.pyplot as plt
import sys
import logging
import numpy as np
from multiprocessing import Queue
from threading import Thread


adapter = pygatt.GATTToolBackend()
rx=[]
ry=[]
rz=[]

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

    # print('Accelerometer = x={} y={} z={}'.format(x_short, y_short, z_short))





def temp_handle(handle, value):
    print(f'received: {value}')




def get_data(mqtt):
    logging.basicConfig()
    logging.getLogger('pygatt').setLevel(logging.DEBUG)

    try:
        adapter.start()
        device = adapter.connect('CF:BE:9E:5F:65:DA', address_type=pygatt.BLEAddressType.random, auto_reconnect=True)
        print('found')
        time.sleep(15)
        print('connected')
        start = time.time()
        while True:
            num = device.char_read_handle('0x27')
            handle_data(handle='0x27', value=num)
            # time.sleep(0.1)

    finally:
        adapter.stop()