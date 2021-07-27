from multiprocessing import Queue
from threading import Thread
from core_funct.data_work import*
from core_funct.serial_util import *
import sys

process_block=100
remind_interval=60

if __name__ == '__main__':
    try:
        mqtt = Queue()                           #创建一个队列
        pro = Thread(target=get_data,args=(mqtt,))
        cus = Thread(target=process_data,args=(mqtt,process_block))
        temp = Thread(target=upload_temperature, args=())
        remind = Thread(target=reminder, args=(remind_interval, ))
        pro.start()
        cus.start()
        temp.start()
        remind.start()
    except:
        sys.exit(0)

