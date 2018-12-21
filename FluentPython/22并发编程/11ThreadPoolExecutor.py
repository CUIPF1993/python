from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time
import queue

detail_url_list =queue.Queue()

def get_detail_url():
    global detail_url_list
    time.sleep(2)
    print("get detail url start")
    for i in range(20):
        url = "http://www.lu/artilce/detail/{id}".format(id=i)
        detail_url_list.put(url)
    print("get detail url end")

def get_detail_html():
    global detail_url_list
    while True:
        time.sleep(3)
        url = detail_url_list.get()
        print("get {}".format(url))

if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=3)
    t = Thread(target=get_detail_url, )
    t.start()

    for i in range(10):
        executor.submit(get_detail_html)

    executor.shutdown()

"""
    executor=ProcessPoolExecutor(max_workers=3)

    futures=[]
    for i in range(11):
        future=executor.submit(task,i)
        futures.append(future)
    executor.shutdown(True)
    print('+++>')
    for future in futures:
        print(future.result())
        """
