from concurrent.futures import ThreadPoolExecutor,as_completed,wait,FIRST_COMPLETED
from concurrent.futures import Future

# Future未来对象，task的返回对象
from functools import wraps
import time

def times(func):
    @wraps(func)
    def inner(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        print("{} running times --> {}".format(func.__name__,time.time()-start))
        return result
    return inner

def get_html(times):
    time.sleep(times)
    print("get page {} success".format(times))
    return  times

@times
def main():
    pool = ThreadPoolExecutor(max_workers=3)
    # 通过submit函数提交执行的函数到线程，submit是立即返回
    L = [2,3,4,2,3,2,5,3,2]
    for i in L:
        pool.submit(get_html,i)

    pool.shutdown()
# get page 2 success
# get page 3 success
# get page 4 success
# get page 2 success
# get page 3 success
# get page 2 success
# get page 2 success
# get page 3 success
# get page 5 success
# main running times --> 9.003904819488525

if __name__ == "__main__":
    main()

