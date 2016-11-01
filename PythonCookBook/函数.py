#用def 定义的函数是所有程序的基石

#7.1编写可以接受任意长度的函数

#编写接受任意数量的位置参数，可以使用以*开头的参数
def avg(first,*rest):
    return (first+sum(rest))/(1+len(rest))
#Sample
avg(1,2)    #1.5
avg(1,2,3,4)    #2.5

#接受任意长度的关键字参数，可以使用以**开头的参数
def anyargs(*args,**kways):
    print(args)     #A tuple
    print(kways)       #A dict

#在这个函数中，所有的位置参数都放置在元组args中，而所有的关键字参数都会被放置在字典中

#7.2编写只接受关键字参数的函数
#如果将关键字参数放置在以*打头的参数或者是一个单独的*之后，这个特性就很容易实现。
def recv(maxsize,*,block):
    'Receives a message'
    pass

# recv(1024,True)
recv(1024,block = True) #OK

#这项技术可以为那些接受任意数量的位置参数的函数来指定关键字参数.
def mininum(*values,clip = None):
    m = min(values)
    if clip is not None:
        m = clip if clip>m else m
    return m

mininum(1,5,2,-5,10)        #Return -5
mininum(1,5,2,-5,10,clip=0)        #Return 0

#7.3讲元素信息附加到函数参数上

#两个整数相加
def add(x:int,y:int) -> int :   
    return x+y

print(help(add))

#Help on function add in module __main__:

#add(x:int, y:int) -> int
#两个整数相加
  
#7.4从函数中返回多个值
def myfun():
    return 1,2,3

a,b,c =myfun()
#它实际上只是创建出一个元组，当调用的函数返回元组，通常会将结果赋值给多个变量，然后简单的元组解包

#7.5定义带有默认参数的函数

def spam(a,b=42):
    print(a,b)

#首先，对默认参数的赋值只会在函数定义的时候绑定一次。
x =42
def spam(a,b =x):
    print (a,b)

spam(1)     #1 42
x = 23      #Has no effect
spam(1)     #1 42

#给默认参数赋值的应该总是不可变的对象，比如None，True，False，数字或者字符串
#示范一个错误的例子
def spam(a,b=[]):
    print(b)
    return b

x =spam(1)      #[]
x.append(99)
x.append('Yow!')

spam(1)     #Modifield list get returned
#[99, 'Yow!']

#正确的示范
def spam(a,b= None):
    if not b:
        b = []

#7.6定义匿名或者内联函数

add = lambda x,y:x + y
print (add(2,3))        #5

#这里用到的lambda表达式与下面的函数定义有着相同的功能
def add(x,y):
    return x+y

#一般来说，lambda表达式可用于在如下的上下文环境中，比如排序或者对数据进行整理
names = ['David Beazley','Brian Jones','Raymond Hettiner','Ned Batchelder']
names = sorted(names,key = lambda name:name.split()[-1].lower())
print(names)
#['Ned Batchelder', 'David Beazley', 'Raymond Hettiner', 'Brian Jones']

#7.7在匿名函数中绑定变量的值

x =10
a = lambda y:x + y
x =20
b = lambda y:x + y
print (a(10))       #30
print (b(10))       #30
#在lambda表达式中用到的x是一个自由变量，在运行时才进行绑定而不是定义的时候绑定

#如果希望匿名函数可以在定义的时候绑定，并保持值不变，那么可以将这个值设置为默认参数。
x =10
a =lambda y,x = x: x+y
x =20
b =lambda y,x = x: x +y
print (a(10))       #20
print (b(10))       #30

#7.8让带有N个参数的可调用对象以较少的参数形式调用
"""
我们有一个可调用对象可能会以回调函数的形式同其他的Python代码交互，但是这个可调用对象需要
的参数过多，如果直接调用的话会产生异常。
解决方案：
如果需要减少函数的参数数量，应该使用functools.partial()。函数partial()允许我们给一个或
多个参数指定固定值，以减少需要提供给之后调用的参数数量。
"""
def spam(a,b,c,d):
    print(a,b,c,d)

from functools import partial
s1 =partial(spam,1)     #a = 1
s1(2,3,4)       #1,2,3,4
s1(4,5,6)       #1,4,5,6

s2 =partial(spam, d = 42)       #d =42
s2(1,2,3)       #1,2,3,42

s3 = partial(spam,1,2,d =42)
s3(4)       #1,2,4,42

#假设有一系列以元组(x,y)来表示的点坐标。可以用下面的的函数来计算两点之间的距离

points = [(1,2),(3,4),(5,6),(6,7),(7,8)]

import math 
def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.hypot(x2-x1,y2-y1)

pt = (4,3)
points.sort(key = partial(distance,pt))
print(points)       #[(3, 4), (1, 2), (5, 6), (6, 7), (7, 8)]

#7.9用函数替代只有摸个方法的类

#7.10在回调函数中携带额外的状态

def apply_async(func,args,*,callback):
    #Compute the result
    result = func(*args)

    #Invock the callBack with the result
    callback(result)

def print_result(result):
    print('Got:',result)

def add(x,y):
    return x+y

apply_async(add,(2,3),callback = print_result)
#Got: 5
apply_async(add,('Hello','world'),callback=print_result)
#Got: Helloworld

#一种在回调函数中携带额外信息的方法是使用绑定方法（bound-method）而不是普通方法

class ResultHandler:
    def __init__(self):
        self.sequence = 0

    #这个类保存一个内部的序列号，每当接收到一个结果时就递增这个号码
    def handler(self,result):
        self.sequence += 1
        print ('[{}] Got:{}'.format(self.sequence,result))

#要使用这个类，可以创建一个实例并将绑定方法handler当回调函数使用
r =ResultHandler()
apply_async(add,(2,3),callback = r.handler)     #[1] Got:5

#作为类的替代方案，也可以使用闭包来捕获状态。示例如下：

def make_handler():
    sequence = 0
    def handler (result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got:{}'.format(sequence,result))
    return handler

handler = make_handler()
apply_async(add,(2,3),callback = handler)     #[1] Got:5

#除此之外，有时候利用协程（coroutine）来完成同样任务
def make_handler():
    sequence =0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got:{}'.format(sequence,result))

handler = make_handler()
next(handler)
apply_async(add,(2,3),callback = handler.send)     #[1] Got:5

#可以通过额外的参数在回调函数中携带状态，然后用partial（）来处理这个参数

class SequenceNo:
    def __init__(self):
        self.sequence =0

def handler(result,seq):
    seq.sequence +=1
    print('[{}] Got:{}'.format(seq.sequence,result))

seq = SequenceNo()
apply_async(add,(2,3),callback = partial(handler,seq =seq))     #[1] Got:5

apply_async(add,(2,3),callback =lambda r:handler(r,seq))     #[2] Got:5
"""
基于回调函数的软件设计常常会面临使代码陷入一团乱麻的风险。部分原因是因为从代码发起初始请求开始
到回调执行的这个过程中，回调函数常常是与这个环境相脱离的。
"""

#7.11内联函数  (这一部分不好理解）

def apply_async(func,args,*,callback):
    #Compute the result
    result =func(*args)

    #Invoke the callback with the result
    callback(result)
#这里涉及到一个Async类和inlined_async装饰器

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func,args):
        self.func = func
        self.args = args
"""
本节的核心就在inline_async()装饰器函数中，关键点就是对于生成器函数的所有yield语句装饰器
都会逐条追踪，一次一个。为了做到这点，我们创建了一个队列来保存结果，初始时用None来填充。之
后通过循环将结果从队列中取出。然后发送给生成器，这样就会产生下一次的yield，此时就会接收到
Async的实例。
"""
def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue =Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func,a.args,callback = result_queue.put)
            except StopIteration:
                break
    return wrapper

def add(x,y):
    return x+y

@inlined_async
def test():
    r = yield Async(add,(2,3))
    print (r)
    r =yield Async(add,('hello','world'))
    print(r)
    for n in range(10):
        r =yield Async(add,(n,n))
        print (r)
    print('Goodbye')

test()

#5
#helloworld
#0
#2
#4
#6
#8
#10
#12
#14
#16
#18
#Goodbye

#7.12访问定义在闭包内的变量
"""
一般来说，在闭包内层定义的变量对于外界来说完全是隔离的。但是，可以通过编写存取函数（accessor 
function,即getter/setter方法）并将它们作为函数属性附加到闭包上来提供对内层变量的访问支持
"""

def sample():
    n = 0
    #Closure function
    def func():
         print('n=',n)

    #Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n =value

    #Attach as function attribbutes
    func.get_n =get_n
    func.set_n = set_n
    return func

f = sample()
f()     #n=0
f.set_n(10)
f()     #n=10
"""
首先，nonlocal声明使得编写函数来修改内层变量成为可能。。其次，函数属性能够将存取函数以直
接的方式附加到闭包函数上，它们工作的像实例的方法。
"""

#让闭包模拟成类实例，将内层函数拷贝到一个实例的字典中然后将它返回。示例如下：
