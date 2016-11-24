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



#要在元类中支持这样的关键字参数，需要保证在定义__prepare__()、__new__()以及__init__()方法时使用keyword-onliy参数来指定它们
class MyMeta(type):
    #optional 
    @classmethod
    def __prepare__(cls,name,bases,*,debug = False,synchronize = True):
        #Custom processing
        return super().__prepare__(name,bases)

    #Required
    def __new__(cls,name,bases,ns,*,debug = False,synchronize = True):
        #Custom processing
        return super().__new__(cls,name,bases,ns)

    #Required
    def __init__(self,name,bases,ns,*,debug = False,synchronize = True):
        #Custom processing
        return super().__init__(name,bases,ns)

#但是，在自定义的元类中我们还需要提供额外的关键字参数，
class Spam(metaclass = MyMeta,debug  =True,synchronize = True):
    pass

#9.16在*args和**kwargs上强制规定一种参数签名
"""
我们已经编写了一个使用*args和**kwargs作为参数的函数或者方法，这样使得函数成为通用型（可接受任意数量和类型的参数），
但是，我们也想对传入的参数做检查，看看它们是否匹配了某个特定的函数调用签名。
"""

#关于操作函数调用签名的问题，都应该使用inspect模块中的相应功能
from inspect import Signature
from inspect import Parameter
#Make a signature for a func(x,y=42,*,z = None)
parms = [Parameter('x',Parameter.POSITIONAL_OR_KEYWORD),
         Parameter('y',Parameter.POSITIONAL_OR_KEYWORD,default =42),
         Parameter('z',Parameter.KEYWORD_ONLY,default = None)]

sig = Signature(parms)
print(sig)      #(x, y=42, *, z=None)

#一旦有了签名对象，就可以通过对象的bind()方法轻松的将其绑定到*args和**kwargs上
def func(*args,**kwargs):
    bound_values = sig.bind(*args,**kwargs)
    for name ,value in bound_values.arguments.items():
        print(name,value)

func(1,2,z =3)
#x 1
#y 2
#z 3
func(1)
#x 1
func(y =2,x =1)
#x 1
#y 2
func(1,z =3)
#x 1
#z 3

#9.17在类中强制规定编码约定
#我们的程序由一个庞大的类继承体系组成，我们想强制规定一些编码约定（或者做一些诊断工作），使得维护这个程序的程序员能够轻松一点
#如果相对类的定义进行监控，可以用元类来解决。一个基本的元类可以通过从type中继承，然后重新定义它的__new__()或者__init__()。

class MyMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        #clsname is name of class being defined
        #bases is tuple of base classes
        #clsdict is class dictionary
        return super().__new__(cls,clsname,bases,clsdict)

#另外一种方式是定义__init__():
class MyMeta(type):
    def __init__(self,clsname,bases,clsdict):
        #clsname is name of class being defined
        #bases is tuple of base classes
        #clsdict is class dictionary
        super().__init__(clsname,bases,clsdict)

#要使用元类，一般来说会将其作用到一个顶层基类上，然后让其他子类继承

#下面是一个异想天开的例子，这个元类可以用来拒绝类定义中包含大小写混用的方法名。
class NoMixedCaseMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('Bad attribute name: ' +name)
        return super().__new__(cls,clsname,bases,clsdict)

class Root(metaclass = NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self):      #ok
        pass
    #def foo_Bar(self):     Error

#作为一个更加高级而且有用的例子，下面定义的元类可以检查子类中是否有重新定义的方法，确保它们的调用签名与父类中原始的方法相同

from inspect import signature
import logging

class MatchSignaturesMeta(type):
    def __init__(self,clsname,bases,clsdict):
        super().__init__(clsname,bases,clsdict)
        sup = super(self,self)
        for name , value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            #Get the previous definition (if any) and compare the signatures
            #获取先前的定义（如果有）并比较签名
            prev_dfn = getattr(sup,name,None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    print('Signature mismatch in %s .%s != %s',value.__qualname__,prev_sig,val_sig)

#Example
class Root(metaclass = MatchSignaturesMeta):
    pass

class A(Root):
    def foo(self,x,y):
        pass

    def spam(self,x,*,z):
        pass

class B(A):
    def foo(self,a,b):      #Signature mismatch in %s .%s != %s B.spam (self, x, *, z) (self, x, z)
        pass

    def spam(self,x,z):     #Signature mismatch in %s .%s != %s B.foo (self, x, y) (self, a, b)
        pass

#9.18通过编程的方式来定义类
#我们可以通过使用函数types.new_class()来实例化新的类对象。所以要提供类的名称、父类名组成的元组、关键字参数以及
#一个用来产生类字典(class dictionary)的回调，类字典中包含着类成员。
#stock.py
#Example of marking a class manually from parts

#Methods
def __init__(self,name,shares,price):
    self.name = name 
    self.shares = shares
    self.price = price

def cost(self):
    return self.shares * self.price

cls_dict = {'__init__':__init__,
            'cost':cost,}

#Make class
import types

Stock = types.new_class('Stock',(),{},lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__

#这么做会产生一个普通的类对象，和期望的一样
s = Stock('ACME',50,90.1)
print(s)        #<__main__.Stock object at 0x022E4B90>
print(s.cost())     #4505.0

#下面和命名元组相似

#9.19在定义的时候初始化类成员
#我们想在定义类的时候对部分成员进行初始化，而不是在创建类实例的时候完成。
#在定义类的时候执行初始化或者配置操作是元类的经典用途。从本质上说，元类是在定义类的时候触发执行的，此时可以执行额外的步骤。

#下面的示例采用这种思想创建了一个类似collections模块中命名的元组类：
import operator

class StructTupleMeta(type):
    def __init__(cls,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for n ,name in enumerate(cls._fields):
            setattr(cls,name,property(operator.itemgetter(n)))

class StructTuple(tuple,metaclass = StructTupleMeta):
    _fields = []
    def __new__(cls,*args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required '.format(len(cls._fields)))
        return super().__new__(cls,args)

class Stock(StructTuple):
    _fields = ['name','shares','price']

s = Stock('BOB',30,100)
print (s.shares)        #30

#9.20通过函数注解来实现方法重载  先空过去不看
#本节的思想基于一个简单事实——即，Python允许对参数进行注解

#下面的解决方案正是应对于此，我们使用了元类及描述符来实现：

import inspect
import types

class MultMethod:
    '''
    Represent a single multimethod.
    '''
    def __init__(self,name):
        self._methods = {}
        self.__name__ = name 

    def register(self,meth):
        '''
        Register a new method as  a multimethod
        '''
        sig = inspect.signature(meth)

        #Building a type signature from the method's annotations
        types = []
        for name,param in sig.parameters.items():
            if name == 'self':
                continue
            if param.annotation is inspect.Parameter.empty:
                raise TypeError('Argument {} must be annotated with a type'.format(name))
            if not isinstance(param.annotation ,type):
                raise TypeError('Argument {} annotation must be a type'.format(name))

            if param.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth

            types.append(param.annotation)
        self._methods[tuple(types)] = meth

    def __call__(self,*args):
        '''
        Call a method based on type signature of the arguments
        '''
        types = tuple(type(args) for arg in args[1:])
        meth = self._methods.get(types,None)
        if meth:
            return meth(*args)
        else:
            raise TypeError('No mathing method for types {}'.format(types))

    def __get__(self,instance,cls):
        '''
        Descriptor method needed to make calls work in a class
        '''
        if instance is not None:
            return types.MethodType(self,instance)
        else :
            return self

class MultiDict(dict):
    '''
    Special dictionary to multmethods in a metaclass
    '''
    def __setitem__(self, key,value):
        if key in self:
            #If key already exist,it must bbe a multimethod or callable
            current_value = self[key]
            if isinstance(current_value,MultMethod):
                current_value.register(value)
            else:
                mvalue = MultMethod(key)
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key,mvalue)
        else:
            super().__setitem__(key,value)

class MultipleMeta(type):
    '''
    Metaclass that allows multiple dispatch of methods
    '''
    def __new__(cls,clsname,bases,clsdict):
        return type.__new__(cls,clsname,bases,dict(clsdict))

    @classmethod
    def __prepare__(cls,clsname,baese):
        return MultiDict()

class Spam(metaclass = MultipleMeta):
    def bar(self,x:int,y:int):
        print('Bar 1:',x,y)

    def bar(self,s:str,n:int =0):
        print('Bar 2:',s,n)

#Eample :overloaded __init__
s = Spam()
#s.bar(2,3)  有误

#9.21 避免出现重复的属性方法
#我们正在编写一个类，而我们不得不重复定义一些执行相同任务的属性方法，比如说做类型检查。
#考虑下面这个简单的类，这里的属性都用property方法进行了包装：

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age 
        
    @property
    def name (self):
        return name
    
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('name must be a string')
        self.name = value
        
    @property
    def age (self):
        return self.age
    
    @age.setter
    def age(self,value):
        if not isinstance(value,int):
            raise TypeError('age must be an int')        
        self.age =value 

#我们编写的很多代码仅仅只是强制对属性做类型断言，这时，我们可以通过创建一个函数，让它为我们定义这个属性并返回给我们

def typed_property(name,expected_type):
    storage_name = '_'+name

    @property
    def prop(self):
        return getattr(self,storage_name)

    @prop.setter
    def prop(self,value):
        if not isinstance(value,expected_type):
            raise TypeError('{} must be a {}'.format(name,expected_type))
        setattr(self,storage_name,value)
    return prop

#Example
class Person:
    name = typed_property('name',str)
    age = typed_property('age',int)
    def __init__(self,name,age):
        self.name = name
        self.age = age

# 9.22以简单的方式定义上下文管理器
#我们想实现新形式的上下文管理器，然后在with语句中使用
#编写一个新的上下文管理器，其中最直接的一种方式就是使用contextlib模块中的@contextmanager装饰器
#在下面实例中，我们用上下文管理器来计时代码块的执行时间

import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}:{}'.format(label,end-start))

#Exapmle
with timethis('conting'):
     n = 10000
     while n > 0:
         n -=1
#conting:0.0156252384185791

