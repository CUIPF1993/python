# 讲序列分解为单独的变量
#1.2从任意长度的可迭代对象中分解元素
#‘*’表达式，将可迭代对象的第一个和最后一个去掉，只剩下中间的

L = [1,2,3,4,5,6]
def drop_first_last(items):
    first,*middle,last = items
    return middle

print (drop_first_last(L))

#*式的语法在可迭代的变长元组序列时尤其有用
recrords = [('foo',1,2),('bar','hellow'),('foo',3,4)]

def do_foo(x,y):
    print ('foo',x,y)

def do_bar(s):
    print('bar',s)

for tag,*args in recrords:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)

#1.3保存N个元素
#在迭代对象中或其他形式的处理过程中对最后几项纪录做一个有限的历史纪录。
"""
下面的代码对一系列文本行进行操作，当发现匹配的文本时，就输出当前的匹配行以及
最后检查过的N行文本。
"""
from collections import deque

def search(lines,pattern,history = 5):
    previous_lines = deque(maxlen = history)
    for line in lines:
        if pattern in line:
            yield line,previous_lines
        previous_lines.append(line)

# Example use on a file


with open ("somefile.txt") as f:
    for line,previous_lines in search(f,'python',5):
        for pline in previous_lines:
            print(pline,end = ' ')
        print (line ,end ='')
        print ('-'*20)

"""
deque(maxlen =x)创建了一个固定长度的队列。当有新纪录加入到队列而队列已满时
会自动移除最老的纪录。
"""

q = deque(maxlen = 3)
q.append(1)
q.append(2)
q.append(3)
q.append(4)

print (q)

"""
当需要一个简单队列结构时，如果不指定队列的大小，也就得到一个无边界的队列，可
以在两端执行添加和弹出操作。
"""

q = deque()
q.append(1)
q.append(2)
q.append(3)
q.appendleft(4)

print (q)

q.pop()
q.popleft()

#从队列两端添加或弹出元素的复杂度都为O（1），列表为O(N)。

#1.4 找到最大和最小的N个元素。
"""
heapq模块有两个函数——nlargest()和nsmallest()
"""

import heapq

nums = [1,8,2,23,7,-4,18,23,42,37,2]

print (heapq.nlargest(3,nums))
print (heapq.nsmallest(3,nums))

#这两个函数都可以接受一个参数Key,从而允许他们工作在更加复杂的数据结构上

prtfolio = [ {'name':'IBM','share':100,'price':91.1},
            {'name':'AAPL','share':50,'price':543.22},
            {'name':'FB','share':200,'price':21.09},
            {'name':'HPQ','share':35,'price':31.75},
            {'name':'YHOO','share':45,'price':16.35},
            {'name':'ACME','share':75,'price':115.65}]

cheap = heapq.nsmallest(3,prtfolio,key=lambda s :s['price'])
expensive = heapq.nlargest(3,prtfolio,key=lambda s :s['price'])
for i in  cheap:
    print (i)

#1.5实现优先队列

"""
他能够以给定的优先顺序对元素的优先级别对元素排序，且每次pop操作时都优先返回
优先级别最高的元素
""" 

#下面的类利用heaqp模板实现一个简单的优先队列
#import heaqp

class PriorityQueue:
    
    def __init__(self):
        self._queue =[]
        self._index = 0
        
    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)

q = PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('apam'),4)
q.push(Item('qrok'),1)    

print (q.pop()) 
print (q.pop())    

"""
函数heapq.heappush和heapq.heappop（）分别实现讲元素从列表中插入和移除操
作，且保证列表中第一个元素的优先级最低。heapqpop()总是返回优先级最低的元素。
"""   
#Item实例时无法比较的，但元组可以比较,元组首先比较第一个元素，然后是第二个。
a = (2,Item('foo'),1)
b = (3,Item('bar'),5)
if a<b:
    print ("a<b is ture")
 
#1.6将字典映射到多个值上  
"""
利用collection模块中的defaultdict类，defaultdictde的一个特点就是他会
自动创建初始化第一个值，这样只需要关注添加的元素即可。
"""   

from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['a'].append(4)
print (d)

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['a'].add(4)
print (d)

#使用传统方法，构建一键多值
d ={}
pairs=[(1,2),(2,3),(1,3),(2,4),(3,4),(4,1)]
for key ,value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)
 
#使用defaultdict 后代码：
d = defaultdict(list)
for key,value in pairs:
    d[key].append(value)

#1.7让字典保持有序
"""
使用collections模块中的OrederedDict类。当对字典做迭代时，他会严格按照元
素添加的顺序进行
"""
from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

for key in d:
    print(key,d[key])

#当想构建一个映射结构以便稍后对其做序列化或编码成另一种格式时用OrderedDict
"""
OrderedDict内部维护了一个双向链表，它会根据元素添加的顺序来排列建的位置。第
一个新加的元素被放置在链表末尾。接下来对已存在的元素重新赋值不会改变键的顺序。
"""

#1.8与字典相关的计算问题。

prices = {'ACEM':45.23,'APPL':634,'IBM':205,'HOP':37,'FB':10}

#利用zip()将字典的键和值翻转过来
min_price = min(zip(prices.values(),prices.keys()))

#要对数据排序只要使用zip()再配合sorted()就可以了。
prices_sorted = sorted(zip(prices.values(),prices.keys()))

#注意zip()创建了一个迭代器，它的内用只能被消费一次。

#1.9在两个字典中寻找相同的点

a = {'x':1,'y':2,'z':3}

b = {'w':10,'x':11,'y':2}

#Find keys in common
a.keys() & b.keys() #{'x','y'}

#Find keys in a that are not in b
a.keys() - b.keys() #{'z'}

#Find（key,value)pairs in common
a.items() & b.items() #{('y',2)}

"""
这类型的操作也可以用来修改或过滤掉字典中内容，下面利用列表推导式去掉某些键
"""

c = {key:a[key] for key in a.keys() - {'z','w'}}
#c is {'x':1,'y':2}

"""
字典是一系列键和值之间的映射集合。字典的keys()方法返回keys-view对象，其中
暴露了所有的键。关于字典的键有一个很少人知道的特性，那就是是他们也支持常见得
集合操作，比如求并集、交集、差集。
字典的items()方法返回由（key,value)对组成的items-view对象。这个对象支持
类似的集合操作，可以用来完成找出两个字典间有哪些键值对相同的操作。
"""

#1.10 从序列中移除重复的元素，且保持元素的顺序不变

#如果序列中的值是可哈希（hashable)的，可以通过使用集合和生成器解决

def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

a = [1,2,5,1,9,5,10,2]

list(dedupe(a))

"""
如果一个对象是可哈希的，那么在它的生存期内必须是不可变的，它需要一个__hash__()
方法。整数、浮点数、字符串、元组都是不可变的。
"""
#如果想在不可哈希的对象（比如列表）序列中去除重复项，代码如下：
def dedupe(items , key = None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        #key(item)这个地方不是很懂
        if val not in seen:
            yield item
            seen.add(val)
#这里的参数key 的作用是指定一个函数用来将序列中的元素转换可哈希的类型。

a = [{'x':1,'y':2},{'x':1,'y':3},{'x':1,'y':2},{'x':2,'y':4}]

b = list(dedupe(a,key=lambda d:(d['x'],d['y'])))
print (b)

b = list(dedupe(a,key=lambda d:d['x']))
print (b)

#1.11对切片命名

#内置的slice（）函数会创建一个切片对象，可以用在任何允许进行切片操作的地方。

items = [0,1,2,3,4,5,6,7,8,9]
a =slice(2,4)

print(items[2:4])
print(items[a])

items[a] = [10,11]
print(items)

del items[a]
print(items)

print(a.start)

"""
如果有一个slice对象的实例s,可以分别通过s.start,s.stop以及s.step属性获
取对象相关信息
"""

#1.12找出序列中出现次数最多的元素。

#collections 模块中Counter类，可以使用most_common()方法可以实现。

words = ['look','my','into','eyes','look','into','my','eye',
         'the','look','my','into','my','into','eyes','look',
         'the','look','my',]

from collections import Counter

word_counts = Counter(words)
top_three = word_counts.most_common(3)
print (top_three)

"""
可以给Counter对象提供任何可哈希的对象作为输入。在底层实现中，Counter是一个
字典，在元素和他们出现的次数间做映射。
"""

print(word_counts['look'])

#使用update()

morewords = ['why','are','you','not','looking','in','my','eye']
word_counts.update(morewords)

#关于Counter对象，它可以轻松地同各类数学运算操作结合使用

a =Counter(words)
b = Counter(morewords)

c =a+b
print (c)

d = a-b
print(d)

#1.13通过公共键对字典进行排序
#利用operator模块的itemgetter函数对字典列表进行排序

rows = [{'fname':'Brian','lname':'Jones','uid':1003},
       {'fname':'David','lname':'Beazley','uid':1002},
       {'fname':'John','lname':'Cleese','uid':1001},
       {'fname':'Big','lname':'Jones','uid':1004},]

#根据所有字典的共有字段来对这些记录排序
from operator import itemgetter

rows_by_fname = sorted(rows,key = itemgetter('fname'))
rows_by_uis = sorted(rows,key = itemgetter('uid'))

print (rows_by_fname)
print (rows_by_uis)

#itemgetter()函数还可以接受多个键
rows_by_lfname = sorted(rows,key = itemgetter('lname','fname'))
print (rows_by_lfname)

"""
rows 被传递给内建的sorted()函数，该函数接受一个关键字参数key.这个参数应该
代表一个可调用对象（callable)，该对象从rows中接受一个单独的元素作为输入并
返回一个用以做排序依据的值。
"""

#有时候会用lambda 表达式来取代itemgetter()的功能

rows_by_fname = sorted(rows,key = lambda r:r['fname'])
print (rows_by_fname)

rows_by_lfname = sorted(rows,key = lambda r: (r['lname'],r['fname']))
print (rows_by_lfname)

#itemgetter()同样适合于min()和max()这样的函数

#1.14对不原生支持比较操作的对象排序。

#1.15根据字段将记录分组
#itertools.groupby()函数对数据分组有用。
from itertools import groupby

rows.sort(key = itemgetter('uid'))

for lname ,items in groupby(rows,key = itemgetter('lname')):
    print(lname)
    for i in items:
        print(' ',i)
"""
函数groupby()通过扫描序列找出拥有相同值（或是由参数key指定的函数所返回的值）
的序列项，并将它们分组。groupby()创建一个迭代器，而在每次迭代时都会返回一个
值（value）和一个子迭代器（sub_iterator），这个子迭代器可以产生所有在该分
组内的该项的值。
"""

#1.16筛选元素
#使用列表推导式。

mylist = [1,4,-5,10,2,3,-1,-3,4,6]
a = [n for n in mylist if n > 0]

#使用生成器表达式通过迭代的方式产生筛选结果
pos = (n for n in mylist if n > 0)

#可以将处理筛选逻辑的代码放在一个单独的函数中，然后使用内建的filter()函数处理。

values = ['1','2','N/A','-','4','*-','5']

def is_int(val):
    try :
        x =int(val)
        return True
    except ValueError:
        return False

ivals = list(filter(is_int,values)) #filter()函数创建一个迭代器。

print(ivals)
#对数据进行转换
mylist = [1,4,-5,10,2,3,-1,-3,4,6]
import math
a = [math.sqrt(n) for n in mylist if n>0]
print (a)

clip_neg =[n if n>0 else 0 for n in mylist]
print (clip_neg)

"""
itertolls.compress()接受一个可以迭代的对象以及一个布尔选择器序列作为输入。
输出时，它会给出所有在相应的布尔选择器中为True的可迭代对象元素。
"""

#1.17从字典中提取子集
#利用字典推导式轻松解决

prices = {'ACME':45.23,'AAPL':612.78,'IBM':205.55,
          'HOP':37.10,'FB':10.75}

p1 = {key:value for key,value in prices.items() if value >200}
print (p1)

#1.18将名称映射到序列的元素中
#collections.namedtuple()(命名元组）可以通过名称来访问元素。

from collections import namedtuple

Subscriber = namedtuple('Subscriber',['addr','joined'])
sub = Subscriber('jonesy@example.com','2012-10-19')
print (sub.addr)
print (sub.joined)

#namedtuple的实例与普通元组是可互换的，而且支持所有普通元组所支持的操作
len(sub)
addr,joined = sub

Stock = namedtuple('Stock',['shares','price'])
def computer_cost(records):
    total =0
    for rec in records:
        s = Stock(*rec)
        total+=s.shares*s.price
    return total 

#1.19对数据进行转换和换算操作
nums =[1,2,3,4,5]
s = sum(x*x for x in nums)

#1.20将多个映射合并为单个映射
a ={'x':1,'z':3}
b ={'y':2,'z':4}
from collections import ChainMap
c =ChainMap(a,b)
"""
ChainMap()可接受多个映射然后在逻辑上使它们表现为一个单一的映射结构。
ChainMap只是维护一个记录底层映射关系的列表。
"""
len(c)
list(c.keys())
list(c.values())
#如果有重复的键，那么这里会采用第一个映射中所对应的值。
#同时，修改映射的操作总是会作用在列表的的第一个映射结构上
c['z'] = 10
c['w'] = 40
del c['x']
print (a)   #{'w': 40, 'z': 10}

#作为ChainMap()的替代方案，可以使用update()方法，但它是不会影响前面的

a ={'x':1,'z':3}
b ={'y':2,'z':4}

merged =dict(b)
merged.update(a)

print (merged)  #{'y': 2, 'x': 1, 'z': 3}











