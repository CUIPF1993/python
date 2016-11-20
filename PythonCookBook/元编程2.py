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
#我们









