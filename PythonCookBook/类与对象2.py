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

#8.21 实现访问者模式   11.16
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

class Number(Node):
    def __init__(self,value):
        self.value = value

#之后，我们可以用这些类来构建嵌套式的数据结构。
#Representation of 1+2*(3-4)/5
t1 = Sub(Number(3),Number(4))
t2 = Mul(Number(2),t1)
t3 = Div(t2,Number(5))
t4 = Add(Number(1),t3)

#为了能让处理过程变得通用，一种常见的解决方案就是实现所谓的“访问者模式”。

class NodeVistor:
    def visit(self,node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self,methname,None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self,node):
        raise RuntimeError('No {} method'.format('visit_' +type(node).__name__))

#要使用这个类，程序员从该类中继承并实现各种visit_Name()方法，这里的Name应该由节点的类型来替换。

class Evaluator(NodeVistor):
    def visit_Number(self,node):
        return node.value

    def visit_Add(self,node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self,node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self,node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self,node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self,node):
        return -node.operand

e = Evaluator()
a = e.visit(t4)
print (a)       #0.6

#8.22 实现非递归的访问者模式
#我们使用访问者模式来遍历一个深度嵌套的树结构，但由于超过Python的递归限制而易崩溃。
#巧妙利用生成器有时候可用来消除树的遍历或查找算法中的递归。下面通过堆栈和生成器来驱动计算，完全不使用递归

import types

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

class Number(Node):
    def __init__(self,value):
        self.value = value

#这一部分是重点
class NodeVisitor:
    def visit(self,node):
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last,types.GeneratorType):
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last,Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()

            except StopIteration:
                stack.pop()
        return last_result

    def _visit(self,node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self,methname,None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)
    
    def generic_visit(self,node):
        raise RuntimeError('No {} method'.format('visit_' +type(node).__name__))


class Evaluator(NodeVisitor):
    def visit_Number(self,node):
        return node.value

    def visit_Add(self,node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self,node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self,node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self,node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self,node):
        return -node.operand

#之后，我们可以用这些类来构建嵌套式的数据结构。
#Representation of 1+2*(3-4)/5
t1 = Sub(Number(3),Number(4))
t2 = Mul(Number(2),t1)
t3 = Div(t2,Number(5))
t4 = Add(Number(1),t3)

e = Evaluator()
a = e.visit(t4)
print (a)       #0.6

#上述代码处理简单的表达式是没有问题，但是嵌套太深的话程序会崩溃。现在我们需要把Evaluator改一下
class Evaluator(NodeVisitor):
    def visit_Number(self,node):
        return node.value

    def visit_Add(self,node):
        yield (yield node.left) + (yield node.right)

    def visit_Sub(self,node):
        yield (yield node.left) - (yield node.right)

    def visit_Mul(self,node):
        yield (yield node.left) * (yield node.right)

    def visit_Div(self,node):
        yield (yield node.left) / (yield node.right)

    def visit_Negate(self,node):
        yield -(yield node.operand)

#现在再次尝试
a = Number(0)
for n in range(1,1000):
    a =Add(a,Number(n))

e = Evaluator()
a = e.visit(a)
print(a)

#8.23 在环状数据结构中管理内存
#我们的程序中创建了环状的数据结构（例如树、图、观察者模式等），但是在内存管理上却遇到了困难。
#环状数据结构的一个简单例子就是树，这里的父节点指向它的孩子，而孩子节点又会指向它们的父节点。
#对于这样的代码，我们应该考虑让其中一条连接使用weakref库中提供的弱引用机制。

import weakref

class Node:
    def __init__(self,value):
        self.value = value
        self._parent = None
        self.children = [] 

    def __repr__(self):
        return 'Node ({!r:})'.format(self.value)

    #property that manages the parent as a weak-reference
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()

    @parent.setter
    def parent(self,node):
        self._parent = weakref.ref(node)

    def add_child(self,child):
        self.children.append(child)
        child.parent = self

root = Node('parent')
c1 = Node('child')
root.add_child(c1)
print(c1.parent)        #Node ('parent')
print(c1)       #Node ('child')
print(root.parent)      #None
del root
print(c1.parent)        #None

#8.24让类支持比较操作
#要支持 >= 操作符，可以在类中定义一个 __ge__()方法。但是如果实现每种可能的比较操作，会变得很复杂
#functools.total_ordering装饰器可以简化这个过程。使用它，可以用它装饰一个类，然后定义__eq__()以及
#另外一个比较方法(__It__、__le__、__gt__或者__ge__)。那么装饰器就会自动为我们实现其他的比较方法。

#作为示例、
from functools import total_ordering
class Room:
    def __init__(self,name,length,width):
        self.name = name 
        self.length = length
        self.width = width
        self.square_feet = self.length*self.width

@total_ordering
class House:
    def __init__(self,name,style):
        self.name = name 
        self.style =style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self,room):
        self.rooms.append(room)

    def __str__(self):
        return'{}:{} square foot {}'.format(self.name,self.living_space_footage,self.style)

    def __eq__(self,other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self,other):
        return self.living_space_footage < other.living_space_footage

#这里，House类已经用@total_ordering来进行装饰。我们定义了__eq__()和__lt__()来根据房子的总面积对房子进行比较
#Build a few house,and rooms to them
h1 = House('h1','Cap')
h1.add_room(Room('Master Bedroom',14 ,12))
h1.add_room(Room('Living Room',18 ,20))
h1.add_room(Room('Kithen',12 ,16))
h1.add_room(Room('Office',12 ,12))

h2 = House('h2','Cap')
h2.add_room(Room('Master Bedroom',14 ,12))
h2.add_room(Room('Living Room',28 ,20))
h2.add_room(Room('Kithen',14 ,16))
h2.add_room(Room('Office',12 ,12))

print(h1<h2)        #True

#8.25创建缓存实例
#当创建类实例时我们想返回一个缓存引用，让其指向上一个用同样参数（如果有的话）创建出的类实例。
import logging
a = logging.getLogger('foo')
b = logging.getLogger('bar')

a is b      #False
c = logging.getLogger('foo')
a is c      #True

#要实现这一行为，应该使用一个与类本身相分离的工厂函数。
#The class in question
class Spam:
    def __init__(self,name):
        self.name = name

#Caching support
import weakref
_spam_cache = weakref.WeakValueDictionary()

def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s 

a = get_spam('foo')
b = get_spam('bar')

print (a is b)      #False

c = a = get_spam('foo')
print (a is c)      #True







