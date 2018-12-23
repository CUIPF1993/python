from multiprocessing import Process
from concurrent.futures import Future,ThreadPoolExecutor,wait

ex = ThreadPoolExecutor(max_workers=3)
ex.submit()


