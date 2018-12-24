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

pool = ThreadPoolExecutor(max_workers=3)

L = [2,3,4,2,3,2,5,3,2]
# ThreadPoolExecutor对象submit对象立即返回一个future对象。

#############

#######################
futures =[pool.submit(get_html,i) for i in L]
for future in as_completed(futures):
    data = future.result()
    print("result: {}".format(data))
pool.shutdown()


# get page 2 success
# result: 2
# get page 3 success
# result: 3
# get page 4 success
# result: 4
# get page 2 success
# result: 2
# get page 2 success
# get page 3 success
# result: 2
# result: 3
# get page 2 success
# result: 2
# get page 3 success
# get page 5 success
# result: 5
# result: 3

"""
1.Future类的对象的实例都表示可能完成或者尚未完成的延迟计算。这与Twisted引擎中的Deferred类，Tornado框架中的Future类类似。
2.期物封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或者抛出异常）后可以获取结果（或异常）
"""
class Future(object):
    def __init__(self):

        self._condition = threading.Condition()
        self._state = PENDING
        self._result = None
        self._exception = None
        self._waiters = []
        self._done_callbacks = []


class ThreadPoolExecutor(_base.Executor):

    # Used to assign unique thread names when thread_name_prefix is not supplied.
    _counter = itertools.count().__next__

    def __init__(self, max_workers=None, thread_name_prefix=''):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
        """
        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")
        # 线程池的线程数目
        self._max_workers = max_workers
        # 任务对列
        self._work_queue = queue.Queue()
        # 存放线程的地方
        self._threads = set()
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))


    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')

            # 1.生成一个Future 对象
            f = _base.Future()
            # 2.生成一个_WorkItem对象
            w = _WorkItem(f, fn, args, kwargs)
            # 3.将_WorkItem对象压入线程安全的队列中
            self._work_queue.put(w)
            # 4.根据线程池的运行情况决定是否启动线程
            self._adjust_thread_count()
            return f

    def _adjust_thread_count(self):
        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)
        # TODO(bquinlan): Should avoid creating new threads if there are more
        # idle threads than items in the work queue.
        num_threads = len(self._threads)
        # 5.根据线程池的线程数目决定是否启动新的线程
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
            # 6.启动新的线程，函数是_worker，参数是提交的存放的_WorkItem队列
            t = threading.Thread(name=thread_name, target=_worker,
                                 args=(weakref.ref(self, weakref_cb),
                                       self._work_queue))
            t.daemon = True
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

class _WorkItem(object):
    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            # 9.获取运算结果
            result = self.fn(*self.args, **self.kwargs)
        except BaseException as exc:
            self.future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None
        else:
            # 将运算结果存放为Future的实例中
            self.future.set_result(result)

def _worker(executor_reference, work_queue):
    try:
        while True:
            # 7.从队列中获取任务
            work_item = work_queue.get(block=True)
            if work_item is not None:
                # 8.调用_WorkItem实例的run方法
                work_item.run()
                # Delete references to object. See issue16284
                del work_item
                continue
            executor = executor_reference()
            # Exit if:
            #   - The interpreter is shutting down OR
            #   - The executor that owns the worker has been collected OR
            #   - The executor that owns the worker has been shutdown.
            if _shutdown or executor is None or executor._shutdown:
                # Notice other workers
                work_queue.put(None)
                return
            del executor
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)