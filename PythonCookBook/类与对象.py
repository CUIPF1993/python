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




    

    


