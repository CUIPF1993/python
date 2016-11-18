"""
软件开发中最重要的一条真理就是“不要重复自己的工作”。也就是说，任何时候当需要创建高度重复的代码(或者
需要复制粘贴源代码）时，通常都需要寻找一个更加优雅的解决方案。在Python中，这类问题常常归结为“元编程”。
"""

#9.1给函数添加一个包装
#我们想给函数添加一个包装层(wrapper layer) 以添加额外的处理（例如，记录日志、计时统计）。
#如果需要用额外的代码对函数做包装，可以定义一个装饰器函数。

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time
    '''
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(func.__name__,end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    while n > 0:
        n -= 1

countdown(1000)     #countdown 0.002005338668823242

#9.2编写装饰器时如何保存函数的元数据
#我们已经编写好一个装饰器，但是当将它用在一个函数上时，一些重要的元数据比如函数名、文档字符串、
#函数注解以及调用签名都会丢失。

#每当定义一个装饰器时，应该总是记得为底层的包装函数添加functools库中的@wraps装饰器
def timethis(func):
    '''
    Decorator that reports the execution time
    '''
    @wraps(func)        #避免元数据丢失
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(func.__name__,end-start)
        return result
    return wrapper

@timethis
def countdown(n:int):
    '''
    sdafasdg
    '''
    while n > 0:
        n -= 1

print(countdown.__name__)       #countdown
print(countdown.__doc__)        #sdafasdg
print(countdown.__annotations__)        #{'n': <class 'int'>}

"""
@wraps装饰器的一个重要特性就是它可以通过__wrapped__属性来访问被包装的那个函数。
__wrapped__属性的存在同样使得装饰器函数可以合适的将底层被包装函数的签名暴露出来。
"""

#9.3对装饰器进行解包装
#我们已经把装饰器添加到一个函数上了，但是想“撤销”它，访问未经过包装的那个原始函数。

#假设装饰器的实现中已经使用了@wraps,一般来说我们可以通过访问__wrapped__属性来获取对原始函数的访问
@timethis
def add(x,y):
    return x+y

orig_add = add.__wrapped__
orig_add(3,4)

#9.4定义一个可接受参数的装饰器
#假设我们想编写一个为函数添加日志功能的装饰器，但是又允许用户指定日志的等级以及一些其他的细节作为参数。

from functools import wraps

def logged(level , name = None,message = None):
    '''
    '''