import logging
from extract_util import *
import numpy as np
import struct
import time
import pygatt
import os
import pickle
import sklearn
import psycopg2 as psy
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
            # temperature = device.char_read_handle('0x2d')
            xyz = handle_data(handle='0x27', value=num)
            # temperature = temperature[0]

            mqtt.put(xyz)
            # time.sleep(0.1)

    finally:
        adapter.stop()


def process_data(mqtt, block_num):
    with open('./model/svmModel.pkl', 'rb') as file:
        svm = pickle.load(file)


    #database
    try:
        db = psy.connect(database='Smart_bottle', user='postgres', password='123456', host='192.168.3.116',
                         port='5432')

        cur = db.cursor()
        x_data=[]
        y_data=[]
        z_data=[]
        cnt=0
        while True:
            print(cnt)
            if len(x_data) < block_num:
                read = mqtt.get()

                temperature=0
                t_xyz = read
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
            # np.save('new_new_dataset4.npy', my_data)
            # os._exit(1)

            tx = low_pass_filter(x_pro, 3)
            ty = low_pass_filter(y_pro, 3)
            tz = low_pass_filter(z_pro, 3)
            valley = valley_detection(tx, 0.001, 2, 0.2)
            check = threshold(tx, ty, tz, valley, 10, 0.4)
            plt.plot(-tx+1)
            plt.scatter(valley, -tx[valley]+1, color='r')
            plt.axhline(y=0.4)
            plt.show()

            for i in range(len(check)):
                c = check[i]
                cx = c[0]
                cy = c[1]
                cz = c[2]

                theta = np.arctan(np.square(cy ** 2 + cz ** 2) / cx)
                alpha = np.arctan(cz / cy)
                theta = (np.rad2deg(theta) + 180) % 180
                alpha = np.rad2deg(alpha)

                safe = sip_bound(alpha, 7)
                raw_feature = feature_engineering(theta[safe[0]:safe[1] + 1])
                t_feature = transform_data(raw_feature)
                t_feature = np.abs(np.array(t_feature))
                amt = predict_amt(t_feature,svm)

                cur.execute("""insert into drinking(time, drinking_amount, temperature) VALUES ('%s', %f, %f)""" % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), amt, temperature))

                cur.execute("commit")

                print(f'You drank {amt}g water.')

            cnt=0
            x_data.clear()
    except Exception:
        print(Exception.message)
