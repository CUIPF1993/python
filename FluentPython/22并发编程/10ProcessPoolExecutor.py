from concurrent.futures import ProcessPoolExecutor
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
    t = Thread(target=get_detail_url, )
    t.start()
    executor = ProcessPoolExecutor(max_workers=3)


    for i in range(10):
        executor.submit(get_detail_html)

    executor.shutdown()

"""
    p=ProcessPoolExecutor(3)
    for url in urls:
        p.submit(get_page,url).add_done_callback(parse_page) #parse_page拿到的是一个future对象obj，需要用obj.result()拿到结果
"""
