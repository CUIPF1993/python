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
import logging

def logged(level , name = None,message = None):
    '''
    Add logging to a function. level is the logging level,name is the logger
    name,and message id the log message .If name and message aren't specified ,
    they default to function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg =message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args,**kwargs):
            log.log(level,logmsg) 
            return func(*args,**kwargs)
        return wrapper
    return decorate

#Example
@logged(logging.DEBUG)
def add(x,y):
    return x+y
add(2,3)

#9.5 定义一个属性可由用户修改的装饰器

#我们想编写一个装饰器来包装函数，但是可以让用户调整装饰器的属性，这样在运行时能够控制装饰器的行为。
#为解决上面的问题，引入了访问器函数(accessor funvtion),通过使用nonlocal关键字声明变量来修改
#装饰器内部的属性，之后把访问器函数作为函数属性附加到函数上。

from functools import wraps,partial
import logging

#Utility decrator to attch a function as anattribute of obj
def attach_wrapper(obj,func = None):
    if func == None:
        return partial(attach_wrapper,obj)
    setattr(obj,func.__name__,func)
    return func

def logged(level,name = None,message = None):
    '''
    Add logging to a function. level is the logging level,name is the logger
    name,and message id the log message .If name and message aren't specified ,
    they default to function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg =message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args,**kwargs):
            log.log(level,logmsg) 
            return func(*args,**kwargs)

        #Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate

#Example
@logged(logging.DEBUG)
def add(x,y):
    return x+y

@logged(logging.CRITICAL,'example')
def spam():
    print('Spam')

import logging
logging.basicConfig(level = logging.DEBUG)
add(2,3)        #DEBUG:__main__:add

add.set_message('Add called')  
add(2,3)        #DEBUG:__main__:Add called

#9.6定义一个能够接受可选参数的装饰器
"""
我们想编写一个单独的装饰器，使其既可以像@decorator 这样不带参数使用，也可以像@decorator(x,y,z)
这样接受可选参数。但是由于简单装饰器和可选参数的装饰器之间存在不同的协调约定。
"""    
from functools import wraps,partial
import logging

def logged(func =None,*,level = logging.DEBUG,name = None,message = None):
    if func == None:
        return partial(logged,level = level,name = name , message = message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg =message if message else func.__name__
        
    @wraps(func)
    def wrapper(*args,**kwargs):
        log.log(level,logmsg) 
        return func(*args,**kwargs)
    return wrapper

#Example
@logged()
def add(x,y):
    return x+y

@logged(level = logging.CRITICAL,name = 'example')
def spam():
    print('Spam')

#9.7利用装饰器对函数参数强制执行类型检查

from inspect import signature
from functools import wraps

def typeassert(*ty_args,**ty_kwargs):
    def decorate(func):
        #If in optimized mode ,disable type checking
        if not __debug__:
            return func
        
        #Map function argument names to suppied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args,**ty_kwargs).arguments
        
        @wraps(func)
        def wrapper(*args,**kwargs):
            bound_values = sig.bind(*args,**kwargs)
            
            #Enforce type asserions across supplied arguments
            for name,value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value,bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name,bound_types[name]))

            return func(*args,**kwargs)
        return wrapper
    return decorate

@typeassert(int ,z = int)
def spam(x,y,z =42):
    print(x,y,z)
    
spam(1,2,3)     #1,2,3
spam(1,'hellow',3)      #1 hellow 3

#这个装饰器相当灵活，既允许指定函数参数的所有的类型，也可以只指定一部分子集，
#此外，类型既可以通过位置参数来指定，也可以通过关键参数来指定。

#9.8在类中定义装饰器
#我们需要理清装饰器是以实例方法还是以类方法的形式应用

from functools import wraps

class A:
    #Decorator as an instance metmod
    def decorator1(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('Decoator 1')
            return func(*args,**kwargs)
        return wrapper

    #Decorator as a class method
    @classmethod
    def decorator2(cls,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('Decoator 2')
            return func(*args,**kwargs)
        return wrapper

#As an instance method
a =A()
@a.decorator1
def spam():
    pass

#As a class method
@a.decorator2
def grok():
    pass

spam()      #Decoator 1
grok()      #Decoator 2

#9.9把装饰器定义成类。
#我们需要装饰器既能在类中工作，又能在类外部使用
#要把装饰器定义成类实例，需要确保在类中实现__call__()和__get__()方法
import types
from functools import wraps

class Profiled:
    def __init__(self,func):
        wraps(func)(self)
        self.ncalls = 0 

    def __call__(self,*args,**kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args,**kwargs)

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self,instance)

#要使用这个类，可以像一个普通的装饰器一样，要么在类中要么在类外部使用
@Profiled
def add(x,y):
    return x+y

class Spam:
    @Profiled
    def bar(self,x):
        print(self,x)

add(2,3)
add(3,4)
print(add.ncalls)       #2
s = Spam()
s.bar(3)        #<__main__.Spam object at 0x030E3F30> 3

#9.10把装饰器作用在类和静态方法上
#将装饰器作用在类和静态方法上是简单而直接的，但是要保证装饰器在应用的时候需要放在@classmethod和@staticmethod之前

import time
from functools import wraps



        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 