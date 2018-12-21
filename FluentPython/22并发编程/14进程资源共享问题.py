from multiprocessing import Process
import time
from threading import Thread

"""
进程是资源分配的最小单位，故每个进程都有自己独立的资源分配(会拷贝一份父进程的资源,与父进程资源相互独立)
"""

n = 0
def add():
    global n
    time.sleep(2)
    for i in range(10):
        n+=i

if __name__ == "__main__":
    p = Process(target=add)
    p.start()
    p.join()
    print(n)    # o

    t = Thread(target=add)
    t.start()
    t.join()
    print(n)    # 1