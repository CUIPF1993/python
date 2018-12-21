# from threading import Thread
# from threading import Semaphore
# from threading import Lock,RLock
#
#
#
# class XiaoAi(Thread):
#     def __init__(self,lock):
#         super().__init__(name="小爱")
#         self.lock =lock
#
#     def run(self):
#         for i in range(0,20,2):
#             self.lock.acquire()
#             print("{} say: {}".format(self.name,i))
#             self.lock.release()
#
# class TianMao(Thread):
#     def __init__(self,lock):
#         super().__init__(name="天猫精灵")
#         self.lock = lock
#
#     def run(self):
#         for i in range(1,20,2):
#             self.lock.acquire()
#             print("{} say: {}".format(self.name,i))
#             self.lock.release()
#
#
# if  __name__ == "__main__":
#     lock = Lock()
#     lock = RLock()
#
#     xiaoai = XiaoAi(lock)
#     tianmao = TianMao(lock)
#     xiaoai.start()
#     tianmao.start()

from threading import Thread,Condition


# 通过threding。condation 完成对话
class XiaoAi(Thread):
    def __init__(self, cond):
        super().__init__(name="小爱")
        self.cond = cond

    def run(self):
        with self.cond:
            for i in range(0, 20, 2):
                print("{} say: {}".format(self.name, i))
                self.cond.notify()
                self.cond.wait()


class TianMao(Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            for i in range(1, 20, 2):
                print("{} say: {}".format(self.name, i))
                self.cond.notify()
                self.cond.wait()


if __name__ == "__main__":
    cond = Condition()

    xiaoai = XiaoAi(cond)
    tianmao = TianMao(cond)
    # 启动顺序很重要 ,先调用wait的线程
    # conditon 有两层锁，一把底层锁会在线程调用了wait方法的时候释放，
    # 上面的锁会在每次调用wait方法的时候分配一把并放入放到cond等待队列中，等待notify方法通知释放锁。
    tianmao.start()
    xiaoai.start()