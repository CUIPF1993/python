# 一个简单的属性描述符实例
class Field:
    """
    
    """
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.name = "{}{}".format(prefix,index)
        cls.__counter+=1

    def __get__(self,instance,owner):
        if instance is None:
            return self
        return getattr(instance,self.name)

    def __set__(self,instance,value):
        instance.__dict__[self.name]=value

class User:
    name = Field()
    age = Field()

    def __init__(self,name,age):
        self.name = name
        self.age = age

user = User(12,12)
print(user.name)

"""
如果user 是某个类的实例，那么user.age（以及等价的getattr(user,'age')),
首先调用__getattribute__。如果类定义了__getattr__方法，
那么在_getattribute__抛出AttributeError的时候就会调用到__getattr__，
而对于描述符(__get__)的调用，则是发生在__getattribute__内部的。
user = User(),那么user.age的查找顺序如下：
(1)如果'age'是出现在User或者其基类的__dict__中，且age是data descriptor（数据描述符），那么调用其__get__方法。否则
(2)如果'age'出现在user的__dict__中，那么直接返回user.__dict__['age'],否则
(3)如果'age'是出现在User或者其基类的__dict__中
    (3.1)如果'age'是non-data description ,那么调用其__get__方法，否则
    (3.2)返回user.__dict__['age']
(4)如果User有__getattr__方法，调用__getattr__方法，否则抛出AttributeError
"""


class NonDesc:
    """

    """
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.name = "{}{}".format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        return "non-data description"


class DataDesc:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.name = "{}{}".format(prefix,index)
        cls.__counter+=1

    def __get__(self,instance,owner):
        return "data description"

    def __set__(self,instance,value):
        instance.__dict__[self.name]=value

class User:
    name = NonDesc()
    User_name = NonDesc()
    class_name = DataDesc()

    def __init__(self,name,class_name):
        self.name = name
        self.class_name = class_name

user = User("boby",'11')
print(user.name)        #boby   (1)
print(user.User_name)       #non-data description   (3)
print(user.class_name)      #data description   (2)









