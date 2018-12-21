# semaphore 是用于控制进入数量的锁

# 做爬虫
# 下面两处都可以
# from threading import Thread,Semaphore
# import time
#
# class HtmlParse(Thread):
#     def __init__(self,id,sema):
#         super().__init__()
#         self.id = id
#         self.sema = sema
#
#     def run(self):
#         self.sema.acquire()
#         time.sleep(2)
#         print("Get article {} sucess".format(self.id))
#         self.sema.release()
#
#
# class UrlProducer(Thread):
#     def __init__(self,sema):
#         self.sema = sema
#         super().__init__()
#
#     def run(self):
#         print("start: ")
#         for i in range(20):
#             html_thread = HtmlParse(i,self.sema)
#             html_thread.start()
#
# if __name__ == "__main__":
#     sema = Semaphore(3)
#     url_thread = UrlProducer(sema)
#     url_thread.start()
#

from threading import Thread,Semaphore
import time

class HtmlParse(Thread):
    def __init__(self,id,sema):
        super().__init__()
        self.id = id
        self.sema = sema

    def run(self):
        time.sleep(2)
        print("Get article {} sucess".format(self.id))
        self.sema.release()


class UrlProducer(Thread):
    def __init__(self,sema):
        self.sema = sema
        super().__init__()

    def run(self):
        print("start: ")
        for i in range(20):
            self.sema.acquire()
            html_thread = HtmlParse(i,self.sema)
            html_thread.start()

if __name__ == "__main__":
    sema = Semaphore(3)
    url_thread = UrlProducer(sema)
    url_thread.start()

