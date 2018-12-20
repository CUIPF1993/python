from threading import Thread
import time

def func():
    for i in range(10):
        time.sleep(1)
        print(i)

if __name__ == "__main__":

    t = Thread(target=func)
    t.daemon = True     # 将子进程设置为守护进程，主进程运行完毕之后，子进程强制停止
    t.start()
    time.sleep(6)

# 0
# 1
# 2
# 3
# 4

