#4.1手动访问迭代器中的内容
items =[1,2,3,4]
#Get the iterator
it = iter(items)
#Run the iterator
next(it)

#4.2委托迭代

class Node:

    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

#Example 
root = Node(0)
child1 =Node(1)
child2 =Node(2)
root.add_child(child1)
root.add_child(child2)
for ch in root:
    print(ch)


#Python的迭代器协议要求__iter__()返回一个特殊的迭代器对象，
#由该对象实现的__next__()方法来完成实际的迭代。


#4,3用生成器创建新的迭代器
def frange(start,stop,increment):
    x =start
    while x<stop :
        yield x
        x+=increment

for n in frange(0,4,0.5):
    print (n)

list(frange(0,1,0.125))

#实现迭代协议
class Node:

    def __init__(self, value):
        self._value = value
        self._children =[]

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)
    #depth_first()首先产生自身，然后迭代每个子节点，利用子节点的depth_first
    #产生其他元素
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

#Example
root = Node(0)
child1 =Node(1)
child2 =Node(2)
root.add_child(child1)
root.add_child(child2)
child1.add_child(Node(4))
child2.add_child(Node(5))

for ch in root.depth_first():
    print (ch)

#4.5反向迭代
a =[1,2,3,4,5]
for i in reversed(a):
    print(i)

#定义反向迭代器
class Countdown:
    def __init__(self,start):
        self.start = start

    #Forword iterator
    def __iter__(self):
        n =self.start
        while n>0:
            yield n
            n-=1
    #Reverse iterator 
    def __reversed__(self):
        n =1
        while n<self.start:
            yield n 
            n+=1

#4.6定义带有额外状态的生成器函数

#4.7对迭代器做切片操作
def count(n):
    while True:
        yield n
        n+=1

c =count(0)
import itertools
for i in itertools.islice(c,10,20):
    print (i)

#4.8跳过可迭代元素的前一部分
from itertools import islice
items = ['a','b','c',1,4,5,7,8]
for i in islice(items,3,None):
    print (i)

#4.9迭代所有可能的组合或排列
"""
itertools.permutations(),它接受一个元素集合，将其中所有的元素重新排列为
所有的可能，并以元组序形式返回。
"""
items = ['a','b','c']
from  itertools import permutations
for p in permutations(items):
    print(p)
#('a', 'b', 'c')
#('a', 'c', 'b')
#('b', 'a', 'c')
#('b', 'c', 'a')
#('c', 'a', 'b')
#('c', 'b', 'a')

#如果想得到较短长度的所有全排列，可以提供一个可选的长度参数
for p in permutations(items,2):
    print (p)
#('a', 'b')
#('a', 'c')
#('b', 'a')
#('b', 'c')
#('c', 'a')
#('c', 'b')

#使用itertolls.combbinations()
from itertools import combinations

for c in combinations(items,3):
    print (c)
#('a', 'b', 'c')

for c in combinations(items,2):
    print (c)
#('a', 'b')
#('a', 'c')
#('b', 'c')

#4.10以索引—值对的形式迭代序列
my_list =['a','b','c']
for idx,val in enumerate(my_list):
    print (idx,val)
#0 a
#1 b
#2 c

#行号从一开始
for idx,val in enumerate(my_list,1):
    print (idx,val)
#1 a
#2 b
#3 c

#4.11同时迭代多个序列
xptx = [1,5,4,2,10,7]
yptx =[2,3,4,5,7,8]
for x,y in zip(xptx,yptx):
    print (x,y)
"""
zip(a,b)的工作原理是创建出一个迭代器，该迭代器可产生出(x,y),这里的x取自序
列a,而y取自序列b。整个迭代的长度和其中最短的输入序列长度相同。
"""

#zip()通常用于需要将不同的数据配对在一起。
headers =['name','shares','price']
values = ['AVEM',100,490.1]

s = dict(zip(headers,values))
for name,value in s.items():
    print (name,value)

#zip()创建出的结果只是一个迭代器。如果需要将配对的数据保存为列表，使用list()

#4.12在不同的列表中迭代
#itertools.chain()方法接受一系列的可迭代对象作为输入并返回一个迭代器。
from itertools import chain

a =[1,2,3,4]
b = ['x','y','z']
for x in chain(a,b):
    print (x)
#1
#2
#3
#4
#x
#y
#z

#4.13创建处理数据的管道

#4.14扁平化处理嵌套型的序列

#使用yield from 语句生成递归生成器函数来解决问题
from collections import Iterable

def flatten(items,ignore_types=(str,bytes)):
    for x in items:
        if isinstance(x,Iterable) and not isinstance(x,ignore_types):
            yield from flatten(x)
        else:
            yield x
"""
isinstance(x,Iterable)检查是否有某个元素是可迭代的。如果是，那么就用yield from
将这个可迭代对象作为一种子例程进行递归。
"""
items = [1,2,[3,4,5],[5,6,[7,8,9]]]
for x in flatten(items):
    print (x)

items = ['Dave',['Thomas','Lewis'],'Paula']
for x in flatten(items):
    print (x)
#Dave
#Thomas
#Lewis
#Paula

#4.15合并多个有效序列，再对整个序列进行迭代

import heapq
a =[1,4,7,10]
b =[2,5,6,11]
for c in heapq.merge(a,b):
    print (c)
#1
#2
#4
#5
#6
#7
#10
#11

#heapq.merge 检查每个输入序列中最小的元素，将最小的输出，重复这个操作.



        


