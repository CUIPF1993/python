import time

import math
# 统计函数的运算时间
def decorate(fun):
    start = time.time()
    def inner(*agrs,**kwargs):
        result = fun(*agrs,**kwargs)
        total = time.time() -start
        print(total)
        return result
    return inner

@decorate
def add():
    total = 0
    for i in range(1000000):
        total+=i

add()   # 0.04188704490661621
print(add)  #<function decorate.<locals>.inner at 0x0000028038B667B8>



# 将所有注册的方法放入同一个列表中
func_list = []
def register(func):
    func_list.append(func)
    return func

@register
def add():
    pass

@register
def sub():
    pass

@register
def mult():
    pass

@register
def mud():
    pass

print([func.__name__ for func in func_list]  )  # ['add', 'sub', 'mult', 'mud']


# 保存函数的元素据
from functools import  wraps

def timethis(func):
    @wraps(func)
    def inner(*args,**kwargs):
        result = func(*args,**kwargs)
        return result
    return inner

@timethis
def func1():
    a = 1
    b = 2

print(func1)    #<function func1 at 0x000001D7BBF266A8>
print(func1.__name__)   #func1
print(func1.__dict__)   #{'__wrapped__': <function func1 at 0x00000259B04B6A60>}

