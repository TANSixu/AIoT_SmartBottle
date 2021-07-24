from multiprocessing import Queue
from threading import Thread
from data_work import*
import sys

process_block=2000


if __name__ == '__main__':
    try:
        mqtt = Queue()                           #创建一个队列
        pro = Thread(target=get_data,args=(mqtt,))
        cus = Thread(target=process_data,args=(mqtt,process_block))
        pro.start()
        cus.start()
    except:
        sys.exit(0)

