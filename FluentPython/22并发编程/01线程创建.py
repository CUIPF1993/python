from threading import Thread
import time

def func(x):
    time.sleep(1)
    print(x)

if __name__ == "__main__":
    for i in range(10):
        t = Thread(target=func,args=(i,))
        t.start()
        #t.join()    # 此处串行
