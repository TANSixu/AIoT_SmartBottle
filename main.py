from multiprocessing import Queue
from threading import Thread
from data_work import*

if __name__ == '__main__':
    mqtt = Queue()                           #创建一个队列
    pro = Thread(target=get_data,args=(mqtt,))
    cus = Thread(target=process_data,args=(mqtt,))
    pro.start()
    cus.start()
