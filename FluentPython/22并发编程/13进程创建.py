from multiprocessing import Process
import os
import time

def func(x):
    time.sleep(1)
    print("子进程id: {},父进程id: {}, 结果为: {}".format(os.getpid(),os.getppid(),x))

if __name__ == "__main__":
    for i in range(10):
        p = Process(target=func,args=(i,))
        p.start()
        #t.join()    # 此处串行
    print("主进程id {}".format(os.getpid()))