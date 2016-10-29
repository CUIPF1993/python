# 讲序列分解为单独的变量
#1.2从任意长度的可迭代对象中分解元素
#‘*’表达式，将可迭代对象的第一个和最后一个去掉，只剩下中间的

L = [1,2,3,4,5,6]
def drop_first_last(items):
    first,*middle,last = items
    return middle

print (drop_first_last(L))

#*式的语法在可迭代的变长元组序列时尤其有用
recrords = [('foo',1,2),
             ('bar','hellow'),
             ('foo',3,4)]

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
函数heapq.heappush和heapq.heappop（）分别实现讲元素从列表中插入和移除
操作，且保证列表中第一个元素的优先级最低。heapqpop()总是返回优先级最低的
元素。
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
pairs=[(1,2),(2,3),(1,3),(2,4),(3,4)(4,1)]
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
