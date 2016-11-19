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

#A simple decorator
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

#Call illustrating application of the decorator to different kinds of method
class Spam:
    @timethis
    def instance_method(self,n):
        print(self,n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls,n):
        print (cls,n)
        while n >0 :
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1

s = Spam()
s.instance_method(1000)
Spam.class_method(1000)
Spam.static_method(1000)

#9.11编写装饰器为包装的函数添加参数
#我们想编写一个装饰器为被包装的函数添加额外的参数。但是添加的参数不能影响到该函数已有的调用约定
#可以使用keyword-only参数将额外的参数注入到函数的调用签名中。

from functools import wraps

def optional_debug(func):
    @wraps(func)
    def wrapper(*args,debug = False,**kwargs):
        if debug:
            print('Calling',func.__name__)
        return func(*args,**kwargs)
    return wrapper

@optional_debug
def spam(a,b,c):
    print(a,b,c)

spam(1,2,3)
#1,2,3
spam(1,2,3,debug = True)    
#Calling spam
#1,2,3

#9.12利用装饰器给类定义打补丁
#我们想检查或修改一部分类定义，以此来修改类的行为，但是不想通过继承或者元类的方式实现
#下面有一个装饰器重写了__getattribute__特殊方法，为其加上日志记录功能

def log_getattribute(cls):
    #Get the original implementation
    orig_getattribute = cls.__getattribute__

    #Make a new defination
    def new_getattribute(self,name):
        print('getting',name)
        return  orig_getattribute(self,name)

    #Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

#Exaample 
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass

a = A(42)
a.x     #getting x
a.spam()        #getting spam

#9.13利用元类来控制市里的创建

#我们想改变实例的创建方式，以此来实现单例模式、缓存或者其他的特性
#假设我们不想让任何人创建出实例：

class NoInstance(type):
    def __call__(self, **kwargs):
        raise TypeError("Can't instantiate directly")
class Spam(metaclass = NoInstance):
    @staticmethod
    def grok(x):
        print('Spam.grok')
        
Spam.grok(42)       #Spam.grok
#a = Spam()    #Can't instantiate directly    

#假设我们想实现单例模式（即，这个只能创建唯一的一个实例）

class Singleton(type):
    def __init__(self, *args,**kwargs):
        self.__instance = None
        super().__init__(*args,**kwargs)  
        
    def __call__(self,*args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args,**kwargs)
            return self.__instance
        else:
            return self.__instance
        
#example 
class Spam(metaclass = Singleton):
    def __init__(self):
        print('Creating Spam')

#这个类只能创建出唯一的实例。        
a = Spam()
b = Spam()
print(a is b)       #True   

#假设我们想创建缓存实例。我们用一个元类实现

import weakref

class Cached(type):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self,*args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

#Example
class Spam(metaclass = Cached):
    def __init__(self,name):
        print('Creating Spam ({!r})'.format(name))
        self.name = name

a = Spam('Guido')
b = Spam('Diana')
c = Spam('Guido')
print(a is b)       #False
print(a is c)       #True

#9.14获取类型属性的定义顺序
#我们想自动记录下属性和方法在类中定义的顺序，这样就能利用这个顺序来完成各种各样操作（例如序列化处理、将属性映射到数据库中等）
#要获取类定义体中的有关信息，可以通过元类来轻松实现。
#下面的例子中，元类使用OrderedDict（有序字典）来获取描述符定义的顺序：

from collections import OrderedDict

#A set of descriptors for various types
class Typed:
    _expected_type = type(None)
    def __init__(self,name = None):
        self._name = name

    def __set__(self,instance,value):
        if not isinstance(value,self._expected_type):
            raise TypeError('Expected '+str(self._expected_type))
        instance.__dict__[self._name] = value

class Integer(Typed):
    _expected_type = int

class Float(Typed):
    _expected_type = float

class String(Typed):
    _expected_type = str

#Metaclass that used an orderedDict for class body
class OrderedMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        d = dict(clsdict)
        order = []
        for name,value in clsdict.items():
            if isinstance(value,Typed):
                value._name = name
                order.append(name)
        d['_order'] = order
        return type.__new__(cls,clsname,bases,d)

    @classmethod
    def __prepare__(cls,clsname,bases):
        return OrderedDict()

class Structure(metaclass = OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self,name))for name in self._order)

#Example  use
class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()
    def __init__(self,name,shares,price):
        self.name = name 
        self.shares = shares
        self.price =price

s = Stock('Good',100,23.33)
#s = Stock('Good','100',23.33)
#TypeError: Expected <class 'int'>
"""
本节的全部核心就在__prepare__()方法上，该特殊方法定义在元类OrderedMeta中，该方法会在类定义一开始的时候
立刻得到调用，调用时以类名和基类名称作为参。它必须返回一个映射型对象(mapping object)供处理类定义体时使用。
由于返回类型OrderDIct实例而不是普通字典，因此类中各个属性间的顺序就是可以方便地得到维护。
"""

#9.15定义一个接受可选参数的元类。
#我们想定义一个元类，使得在定义类的时候提供可选的参数。这样的话在创建类型的时候可以对处理过程进行控制或配置

#在定义类的时候，Python允许我们在class 语句中通过使用metaclass关键字参数来指定元类。

from abc import ABCMeta
from abc import abstractmethod

class Istream(metaclass = ABCMeta):
    @abstractmethod
    def read(self,maxsize = None):
        pass

    @abstractmethod
    def write(self,data):
        pass



