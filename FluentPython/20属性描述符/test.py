import numbers
import re
a = 12


a = re.fullmatch("",'ab')
print(type(a))
print(a)


a = {'name':'cui', 'age':12}
print(a.get('name'))
print(a.get("dfd"))
b = a.pop('name')
print(b)
print(a)

from collections import defaultdict

a = defaultdict(list)
a['d'].append(12)
print(a)

def add(x:int,y:int):
    return x+y

print(add('a','b'))

if 0:
    print('fdfdf')
if not 0:
    print('ddddddddd')