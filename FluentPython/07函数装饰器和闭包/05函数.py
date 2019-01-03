from inspect import signature



a  =1
b =2
def func(x,y:int,z=None,c=0,*args,d,b=12,m=13,**kwargs)->int:
    a
    u =5
    return x+y

print(func.__code__)
print(func.__code__.co_argcount)
print(func.__annotations__)
print(func.__defaults__)
print(func.__globals__)
print(func.__module__)

print(func.__kwdefaults__)
# <code object func at 0x0000023144CFBC90, file "D:/python/FluentPython/07函数装饰器和闭包/05函数.py", line 5>
# 4
# {'y': <class 'int'>, 'return': <class 'int'>}
# (None, 0)
# {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x0000023144CBD160>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'D:/python/FluentPython/07函数装饰器和闭包/05函数.py', '__cached__': None, 'signature': <function signature at 0x0000023144FDBA60>, 'a': 1, 'b': 2, 'func': <function func at 0x0000023144BB1EA0>}
# __main__
# {'b': 12, 'm': 13}


# func(x,y:int,z=None,c=0,*args,d,b=12,m=13,**kwargs)->int:
sig = signature(func)
for name,param in sig.parameters.items():
    print(param.kind,':',name,":",param.default)

# POSITIONAL_OR_KEYWORD : x : <class 'inspect._empty'>
# POSITIONAL_OR_KEYWORD : y : <class 'inspect._empty'>
# POSITIONAL_OR_KEYWORD : z : None
# POSITIONAL_OR_KEYWORD : c : 0
# VAR_POSITIONAL : args : <class 'inspect._empty'>
# KEYWORD_ONLY : d : <class 'inspect._empty'>
# KEYWORD_ONLY : b : 12
# KEYWORD_ONLY : m : 13
# VAR_KEYWORD : kwargs : <class 'inspect._empty'>

class Person:
    pass

def func(p:Person)-> 'hahaha':

    return 123

print(func.__annotations__)
# {'p': <class '__main__.Person'>, 'return': 'hahaha'}