from threading import Thread
import time

class Func(Thread):
    def __init__(self,x):
        super().__init__()
        self.x = x

    def run(self):
        time.sleep(1)
        print(self.x)

if __name__ == "__main__":
    for i in range(10):
        t = Func(i)
        t.start()