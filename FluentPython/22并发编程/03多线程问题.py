from threading import Thread
import time


n = 0
def add():
    global n
    for i in range(1000000):
        n = n +1
    print("add结束")

def sub():
    global n
    for i in range(1000000):
        n = n-1
    print("sub结束")

L = [add,sub]


"""
两个线程同时争抢同一块数据，会发生数据不安全的问题
"""
if __name__ == "__main__":
    p = []
    for func in L:
        t = Thread(target=func)
        t.start()
        p.append(t)

    for t in p:
        t.join()        # 此处是等待主进程运行结束

    print(n)    # -597787
    print("kaishi")