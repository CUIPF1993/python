from threading import Thread,Lock
import time

lock = Lock()

n = 0
def add():
    global n
    for i in range(1000000):
        lock.acquire()
        n = n + 1
        lock.release()
    print("add结束")


def sub():
    global n
    for i in range(1000000):
        lock.acquire()
        n = n - 1
        lock.release()
    print("sub结束")


L = [add, sub]

"""
通过添加锁，来保证数据的安全性。
"""
if __name__ == "__main__":
    p = []
    for func in L:
        t = Thread(target=func)
        t.start()
        p.append(t)

    for t in p:
        t.join()        # 此处是等待主进程，运行结束

    print(n)  # 0