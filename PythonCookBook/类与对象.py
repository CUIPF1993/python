#主题包括让对象支持常见的Python特性。特殊方法的使用、封装、继承、内存管理以及一些有用的设计模式

#8.1修改实例的字符串表示

class Pair:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r},{0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!r},{0.y!r})'.format(self)
"""
特殊方法__repr__返回的实例的代码表示（code representation),通常可以用它的返回的字符串
来重新创建这个实例。内建的repr()函数可以用来返回这个字符串，当缺少交互式解释环境时可用它来
检查实例的值。特殊方法__str__()将实例转换为一个字符串，这样也是str()和print()函数所产生的输出。
"""

p =Pair(3,4)
p #Pair(3,4)   __repr__() output
print (p)       #(3,4)      __str__() output

#特殊的格式化代码！r表示应该使用__repr__()的输出，而不是默认的__str__()
p = Pair(3,4)
print('p is {0!r}'.format(p))       #p is Pair(3,4)
print('p is {0}'.format(p))     #p is (3,4)
"""
对于__repr__(),标准的做法是让它产生的字符串文本能够满足eval(repr(x)) ==x 。如果不可能
办到或者不希望有这种行为，那么应该通常应该让它产生一段有帮助意义的文本，并以<和>括起来。
"""

#8.2自定义字符串的输出格式
#要自定义字符串的输出格式，可以在类中定义__format__()方法。示例如下：
_formats = {'ymd' : '{d.year}-{d.month}-{d.day}',
            'mdy' : '{d.month}-{d.day}-{d.year}',
            'dmy' : '{d.day}-{d.month}-{d.year}'}

class Date:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d = self)
#Date类的实例可以支持如下的格式化操作
d = Date(2012,12,21)

print(format(d))        #2012-12-21
print(format(d,'mdy'))      #12-21-2012

print('The date is {:ymd}'.format(d))       #The date is 2012-12-21
print('The date is {:mdy}'.format(d))       #The date is 12-21-2012

#datetime模块的实例
from datetime import date
d =date(2012,12,21)
print(format(d))        #2012-12-21
print(format(d,'%A,%B,%d,%Y'))      #Friday,December,21,2012

#8.3让对象支持上下文管理协议

#要让对象能够兼容with语句，需要实现__enter__()和__exit__方法。比如说，考虑下面这个表示网络的类
from socket import socket,AF_INET,SOCK_STREAM

class LazyConnection:
    def __init__(self,address,family = AF_INET,type = SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family,self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self,exc_ty,exc_val,tb):
        self.sock.close()
        self.sock = None

from functools import partial

conn = LazyConnection(('www.python.org',80))
#Connection closed

#8.4当创建大量实例时如何节省内存
#对于那些主要用作简单数据结构的类，通常可以在类定义中增加__slot__属性，以此来大量减少对内存的使用。
class Date:
    __solt__ = ['year','month','day']
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

#当定义了__solt__属性时，Python就会针对实例采用一种更加紧凑的内部表示。

#8.5将名称封装到类中。
"""
与其依赖语言特性来封装数据，Python程序员更期望通过特定的命名规则来表达出对数据和方法的用途。
第一个规则是任何已单下划线(_)开头的名字应该总是被认为只属于内部实现。比如：
"""
class A:
    def __init(self):
        self._internal = 0      #An internal attribute
        self.public = 1     #A public attribute
    def public_method(self):
        pass
    def _internal_method(self):
        pass

#以双下划线(__)打头的名称。
class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass
    def public_method(self):

        self.__private_method()

"""
以双下划线打头的名称会导致出现名称重整(name mangling)的行为。具体来说就是上面这个类中的
私有属性会被分别重命名为_B_private和_B_private_method。命名重整的目的在于为了继承——
这样的属性不能通过继承被覆盖。示例如下：
"""
class C(B):
    def __init__(self):
        super().__init__()
        self.__private =1       #Does not override B.__private
    #Dose not overried B.__private_method()
    def __private_method(self):
        pass
#这里，私有名称__private 和__private_mrthod 会被重命名为_C__private 和_C__private_method,这和基类B中的重整命名不同。

#8.6创建可以管理的属性
#在对实力属性的获取和设定上，增加一些额外的处理过程（比如类型检查或者验证）
class Person:
    def __init__(self,first_name):
        self._first_name = first_name

    #Getter function
    @property
    def first_name(self):
        return self._first_name

    #Setter function
    @first_name.setter
    def first_name(self,value):
        if not isinstance(value,str):
            raise TypeError('Excepted a string')
        self._first_name = value

    #Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

a =Person('Guido')
print (a.first_name)        #Guido
#a.first_name =42           Error

#property属性实际上就是将一系列的方法绑定到一起。尽量避免定义大量重复性property的代码

#8.7调用父类中的方法

#我们想调用一个父类中的方法，这个方法在子类中已经被覆盖了，可以使用super()函数来完成。
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()
b = B()
b.spam()
#B.spam
#A.spam

#super()函数的一种常见用途是调用父类的__init__()方法，以确保父类被正确的初始化。
class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

#另外一种常见用途是当覆盖了Python中的特殊用法时，示例如下：
class Proxy:
    def __init__(self,obj):
        self._obj = obj

    #Delegate attribute lookup to internal obj
    def __getattar__(self,name):
        return getattr(self._obj,name)

    #Delegate attribute assigment
    def __serattar__(self,name,value):
        if name.startswitch('_'):
            super().__setattr__(name,value)     #Call original __setattar
        else:
            setattar(self._obj,name,value)

#8.8在子类中扩展属性
#我们想在子类中扩展某个属性功能，而这个属性是在父类中定义的

class Person:
    def __init__(self,name):
        self._name = name
        
    #Getter function
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('Excepted a string')
        self._name = value

    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")

#下面我们从Person类中继承，然后在子类中扩展name属性的功能：
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self,value):
        print ('Setting name to',value)
        super(SubPerson,SubPerson).name.__set__(self,value)

    @name.deleter
    def name(self):
        print ('Deleting name')
        super(SubPerson,SubPerson).name.__delete__(self)

s = SubPerson('Guido')
s.name      #Getting name
s.name = 'Larry'        #Setting name to Larry

#如果只想扩展属性中的其中一个方法。
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name

#或者
class SubPerson(Person):
    @Person.name.setter
    def name(self):
        print ('Setting name to',value)
        super(SubPerson,SubPerson).name.__set__(self,value)

#8.9创建一种新形式的类属性和实例属性

#我们想创建一种新形式的实例属性，它可以拥有一些额外的功能，比如类型检查
#Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self,name):
        self.name = name

    def __get__(self,instance,cls):
        if instance == None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self,instance,value):
        if not isinstance(value,int):
            raise TypeError('Except an int')
        instance.__dict__[self.name] = value

    def __delete(self,instance):
        del instance.__dict__[self.name]

#要使用一个描述符，我们把描述符的实例放置在类的定义中作为类变量来使用。
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x,y):
        self.x = x
        self.y = y 
#当这么做的时，所有针对描述符属性（即，这里的x,y ）访问都会被__get__()、__set__()、和__delete__()方法所捕获。
p = Point(2,3)
p.x         #2  Calls Point.x__get__(p,Point)
p.y = 5         #Call Point.y.__set__(p,5)
#p.x = 2.3       #Call Point.x.__set__(p,2.3)
#'Except an int

#8.10让属性具有惰性求值的能力
#我们将一个只读的属性定义为property属性方法，只有在访问它时才参与计算。但是，一旦访问该属性，我们希望把计算的值
#缓存起来，不用每次访问它时都重新计算。

class lazyproperty:
    def __init__(self,func):
        self.func = func

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

#还用上述代码
import math

class Circle:
    def __init__(self,radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi*self.radius**2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2*math.pi*self.radius

c = Circle(4.0)
c.radius        #4.0

#8.11简化数据结构的初始化过程
#我们编写很多类，把他们当做数据结构来用。但我们厌倦了编写高度重复且样式相同的__init__函数
#通常我们可以将初始化数据结构的步骤归纳到一个单独的__init__()函数中，并将其定义在一个公共的基类中

class Structure:
    #class variabble that specifies expected fields
    _fields = []
    def __init__(self,*args):
        if len(args) != len(self._fields):
            raise TypeError('Except {} arguments'.format(len(self._fields)))

        #Set the arguments
        for name,value in zip(self._fields,args):
            setattr(self,name,value)

class Stock(Structure):
    _fields = ['name','shares','price']

class Point(Structure):
    _fields = ['x','y']

class Circle(Structure):
    _field = ['radius']
    def area(self):
        return math.pi*self.radius **2

s = Stock('ACME',50,91.1)
p = Point(2,3)
print(p.x)      #2

#我们应该提供对关键字参数的支持，这里有几种设计上的悬着。一种选择就是对关键字参数做映射，
#这样他们就只对应于定义在_fields中的属性名。示例如下：
class Structure:
    _fields = []
    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Excepted {} arguments'.format(len(self._fields)))

        #Set all of the positional arguments
        for name,value in zip(self._fields,args):
            setattr(self,name,value)

        #Set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self,name,kwargs.pop(name))

        #Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid argument(s) :{}'.format(','.join(kwargs)))

class Stock(Structure):
    _fields = ['name','shares','price']

s1 = Stock('ACME',50,91.1)
s2 = Stock('ACME',50 , price = 91.1)
s3 = Stock('ACME',price = 91.1,shares = 50)
print(s2.price)         #91.1
print(s3.shares)        #50

#另一种可能的选择是利用关键字参数来给类添加额外的属性，这些额外的属性是没有定义在_field中。示例如下

class Structure:
    #Class variable that specifies excepted fields 
    _fields = []
    
    def __init__(self,*args,**kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        #Set the arguments
        for name,value in zip(self._fields,args):
            setattr(self,name,value)

        #Set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self,name,kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kways)))

class Stock(Structure):
    _fields = ['name','shares','price']

s1 = Stock('ACME',50,91.1)
s2 = Stock('ACME',50 ,91.1,date = '2016')
print(s1.price)         #91.1
print(s2.date)        #2016

#8.12 定义一个接口或者抽象基类
#我们想定义一个类作为接口或者抽象基类，这样可以在此之上执行类型检查并确保在子类中实现特定的方法
#要使用一个抽象基类，可以使用abc模块。
from abc import ABCMeta,abstractmethod

class IStream(metaclass = ABCMeta):
    @abstractmethod
    def red(self,maxbytes = -1):
        pass
    @abstractmethod
    def write(self,date):
        pass

#抽象基类的核心特征就是不能被直接实例化。抽象基类是用来给其他的类当基类使用的，
#这些子类需要实现在基类中要求的方法。抽象基类的主要用途是强制规定所需的编程接口。

"""
我们可能会认为这种形式的类型检查只有在子类化抽象基类（ABC）时才能工作，但是抽象基类也
允许其他的类向其注册，然后实现其接口。
"""
import io
#Register the built-in I/O classes as supporting our interface
IStream.register(io.IOBase)

#Open a normal file and typeee check
f = open('somefile.txt')
if isinstance(f,IStream):
    print ('s')

#@abstractmethod 同样可以施加到静态方法、类方法和property属性上，只要确保以合适的顺序进行即可。

class A(metaclass = ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self,value):
        pass

    @classmethod
    @abstractmethod
    def method1(cls):
        pass

    @staticmethod
    @abstractmethod
    def method2():
        pass

#8.13实现一种数据模型或类型系统

#我们想定义跟种各样的数据结构，但是对于某些特定的属性，我们想对允许付给它们的值强制添加一些限制。
#为了做到这一点，需要对每个属性的设定做定制化处理，因此应该使用描述符来完成
#下面的代码使用描述符实现了一个类型系统的以及对值进行检查的框架：

#Base class. Uses a descriptor to set a value
class Descriptor:
    def __init__(self,name = None,**opts):
        self.name = name
        for key ,value in opts.items():
            setattr(self,key,value)

    def __set__(self,instance,value):
        instance.__dict__[self.name] = value

#Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self,instance,value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Except' + str(self.expected_type))
        super().__set__(instance,value)

#Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self,instance,value):
        if value < 0 :
            raise ValueError('Excepted >= 0')
        super().__set__(instance,value)

class MaxSized(Descriptor):
    def __init__(self,name = None,**opts):
        if 'size' not in opts:
            raise TypeError('missing size options')
        super().__init__(name,**opts)

    def __set__(self,instance,value):
        if len(value) >= self.size:
            raise ValueError('Size must be < ' +str(self.size))
        super().__set__(instance,value)

#这些类可作为构建一个数据模型或者类型系统的基础组件。
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer,Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float,Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizeString(String,MaxSized):
    pass

#有了这些类型对象，现在就可以像这样定义一个类了

class Stock:
    #Specify constraints
    name =SizeString('name',size = 8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('ACME',50,91.1)
print(s.name )      #ACME
#s.name = 'aaaaaaaaaa'         #raise ValueError('Size must be < ' +8)
#s.price = 'aa'          #TypeError: Except<class 'float'>

#可以运用一些技术来简化在类中设定约束的步骤。一般方法是使用类装饰器。

#另外一种方法是使用元类。       P284页有具体做法

#8.14实现自定义的容器

#创建了一个Sequence类，且元素总是以排序后的顺序进行存储。（例子不是很清楚，但能说明大意）
import collections
import bisect

class SortedItems(collections.Sequence):
    def __init__(self,initial = None):
        self._items = sorted(initial) if initial is not None else []

    #Required sequence methods
    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    #Method for adding an item in the right location
    def add(self,item):
        bisect.insort(self._items,item)

items = SortedItems([3,2,1])
print (list(items))     #[1,2,3]
items.add(5)
items.add(4)
print(list(items))      #[1, 2, 3, 4, 5]                 

#8.15 委托属性的访问
#我们想在访问实例的属性时能够将其委托（delegate）到一个内部持有的对象上，这可以作为继承的替代方案。
#简单来说，委托是一种编程模式。我们将某个特定的操作转交给（委托）另外一个不同的对象实现。

class A:
    def spam(self,x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def spam(self,x):
        #Delegate to the internal self._a instance
        return self._a.spam(x)

    def foo(self):
        #Delegate to the internal self._a instance
        return self._a.spam(x)
    def bar(self):
        pass
#如果机油几个方法需要委托，编写像上面那样的代码是非常简单的。但是，如果有许多方法都需要委托，
#另一种实现方式是定义__getattr__()方法，就像下面这样：
class A:
    def spam(self,x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def bar(self):
        pass

    #Expose all of the methods defined on class A
    def __getattr__(self,name):
        return getattr(self._a,name)

#__getattr__()方法能用来查找所有所有的属性。如果代码中尝试访问一个并不存在的属性时，就会调用这个方法。

b =B()
b.bar()     #Call B,bar() (exists on B)
b.spam(42)      #Call B.__getattr__('spam') and delegates to A.spam

#委托的另外一个例子就是在实现代理时。

#A proxy class taht warps around another obbject,bbut exposes its public attributes

class Proxy:
    def __init__(self,obj):
        self._obj = obj

    #Delegate attribute loopup to internal obj
    def __getattr__(self,name):
        print('getattr: ',name)
        return getattr(self._obj,name)

    #Delegate attribute assigment
    def __setattr__(self, name,value):
        if name.startswith('_'):
            super().__setattr__(name,value)
        else:
            print('setattr: ',name,value)
            setattr(self._obj,name,value)

    #Delegate attribte delection
    def __delattr__(self,name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr: ',name)
            delattr(self._obj,name)

#要使用这个代理类，只需要简单地用它包装另外一个实例即可。

class Spam:
    def __init__(self,x):
        self.x = x

    def bar(self,y):
        print('Spam.bar: ',self.x,y)

s = Spam(2)
p = Proxy(s)
print(p.x)      #2
p.bar(3)        #Spam.bar:  2 3

#8.16在类中定义多个构造函数

#我们正在编写一个类，但是想让用户能够以多种方式创建实例，而局限于__init__()提供的这一种。
#要定义一个含有多个构造函数的类，应该使用类方法

import time

class Date:
    #Pimary constuctor
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

    #Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year,t.tm_mon,t.tm_mday)

a = Date(2012,12,21)
b = Date.today()
print(b.year)       #2016

#类方法的一大主要用途就是定义其他可选的构造函数。类方法的一个关键特性就是把类作为其接受的第一个参数（clas）

#8.17不通过调用init来创建实例

#可以直接调用类的__new__()方法来创建一个未经初始化的实例。
class Date:
    #Pimary constuctor
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

d = Date.__new__(Date)

print(d)       #<__main__.Date object at 0x033F4A30>
#print(d.year)       #AttributeError: 'Date' object has no attribute 'year'
#可以看到，得到的实例是未经初始化的。因此，给实例变量设定合适的初始值现在就是我们的责任。
date = {'year':2012,'month':8,'day':29}
for key ,value in date.items():
    setattr(d,key,value)
print(d.year)       #2012

#当需要以非标准的方式创建实例时常常会遇到需要绕过__init__()的情况，比如反序列化数据，或者实现一个类方法将其作为备选的构造函数

#8.18用 Mixin 技术来扩展类定义

#某个库提供了一组基础类以及一些可选的定制方法，如果用户需要的话可以自行添加
#现在假设我们有兴趣将各种各样的定制处理方法（例如，日志记录、类型检查等）添加到映射对象(mapping object)上。

class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """
    __solts__ = ()

    def __getitem__(self,key):
        print('Getting '+str(key))
        return super().__getitem__(key)

    def __setitem__(self,key,value):
        print('Setting {} ={!r}'.format(key,value))
        return super().__setitem__(key,value)

    def __delitem__(self,key):
        print('Deleting '+str(key))
        return super().__delitem__(key)

class SetOnceMappingMixin:
    """
    Only allow a key to be set once.
    """
    __solt__ = ()
    def __setitem__(self,key,value):
        if key in self :
            raise KeyError(str(key) + 'already set')
        return super().__setitem__(key,value)

class StringKeysMappingMixin:
    """
    Restrict keys to strings only
    """
    __solt__ = ()
    def __setitem__(self,key,value):
        if not isinstance(key,str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key,value)

"""
这些类本身是无用的。实际上，如果实例化它们中的任何一个，一点用的事情都做不了（除了会产生异常之外）。
相反，这些类存在的意义是要和其他映射型类通过多重继承的方式混合在一起使用。
"""

class LoggedDict(LoggedMappingMixin,dict):
    pass

d = LoggedDict()
d ['x'] =23     #Setting x =23
d['x']      #Getting x
del d['x']      #Deleting x

#Python 标准库中到处都是mixin类的身影，大部分都是为了扩展其他类的功能而创建的。

#8.19实现带有状态的对象或者状态机
#我们希望实现一个状态机，或者让对象可以在不同的状态中进行操作。但是我们不希望代码中会因此出现大量的条件判断。
#下面这个代表网络连接的类：

class Connection:
    def __init__(self):
        self.state = 'CLOSED'

    def read(self):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('reading')

    def write(self,date):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('writing')

    def open(self):
        if self.state == 'OPEN':
            raise RuntimeError('Already open')
        self.state = 'OPEN'

    def close(self):
        if self.state == 'CLOSED':
            raise RuntimeError('Already closed')
        self.state = 'CLOSED'

"""
这份代码为我们提出了几个难题。首先，由于代码中引入了许多针对状态的条件检查，代码变得复杂。
其次，程序的性能下降了。因为普通的操作如读和写总要在处理前先检查状态。         
"""

#一个更加优雅的方式是将每种操作状态以一个单独的类来定义，然后在Connection类中使用这些状态。

class Connection:
    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self,newstate):
        self._state = newstate

    #Delegate to the state class
    def read(self):
        return self._state.read(self)

    def write(self):
        return self._state.write(self)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

#Connection state base class
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()
  
    @staticmethod
    def close(conn):
        raise NotImplementedError()   

#Implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)
    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')

class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already closed')
    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

c = Connection()
print(c._state)     #raise RuntimeError('Already closed')
#c.read()        #raise RuntimeError('Not open')
c.open()
print(c._state)     #<class '__main__.OpenConnectionState'>
c.read()        #reading

#8.20 调用对象上的方法，方法名字以字符串形式给出。

#对于简单的情况，可以使用getattr()。

import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y 

    def __repr__(self):
        return 'Point({!r},{!r})'.format(self.x,self.y)

    def distance(self,x,y):
        return math.hypot(self.x -x ,self.y - y)

p = Point(3,4)
d = getattr(p,'distance')(0,0)
print(d)        #5.0

#另一种方法是使用operator.methodcaller()
import operator
d = operator.methodcaller('distance',0,0)(p)
print(d)        #5.0

#如果想通过名称来查询方法并提供同样的参数反复调用该方法，那operator.methodcaller是很有用的。

points = [Point(1,2),
          Point(3,0),
          Point(2,2),
          Point(10,2),
          Point(5,2),]
points.sort(key = operator.methodcaller('distance',0,0))
print (points)      #Point(1,2), Point(2,2), Point(3,0), Point(5,2), Point(10,2)]

#8.21 实现访问者模式
#我们需要编写代码来处理或者遍历一个由许多不同的类型的对象组成的复杂数据结构，每种类型的对象处理的方式都不同
#假设我们正在编写一个表示数学运算的程序。

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self,operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(BinaryOperator):
    pass

class Numer(Node):
    def __init__(self,value):
        self.value = value

#之后，我们可以用这些类来构建嵌套式的数据结构。
#Representation of 1+2*(3-4)/5
t1 = Sub(Numer(3),Numer(4))
t2 = Mul(Numer(2),t1)
t3 = Div(t2,Numer(5))
t4 = Add(Numer(1),3)

#为了能让处理过程变得通用，一种常见的解决方案就是实现所谓的“访问者模式”。


