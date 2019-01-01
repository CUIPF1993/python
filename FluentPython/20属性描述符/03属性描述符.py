import abc
import numbers
import re

class Field:
    """
    定义一个属性描述符抽象类，其中_validate方法用于在设置值的时候，验证数据的有效性，
    子类不用实现__get__(),__set__()方法就可以完整实现一个属性描述符类
    """
    __counter = 0

    def __init__(self,*args,**kwargs):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.name = "{}{}".format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self._validate(value)
        instance.__dict__[self.name] = value

    @abc.abstractmethod
    def _validate(self,value):
        """
        定义一个抽象方法，用于验证数据是否合格
        :param value:
        :return:
        """

class FloatField(Field):
    """
    整数数据描述符
    """
    _data_type = numbers.Real
    def __init__(self,*args,min=None,max=None,**kwargs):
        if not isinstance(min,self._data_type):
            raise TypeError('min must be {}'.format(self._data_type.__name__))
        if not isinstance(max, self._data_type):
            raise TypeError('max must be {}'.format(self._data_type.__name__))
        if min > max :
            raise ValueError("must (min <= max)")

        self.min = min
        self.max = max
        super().__init__(*args,**kwargs)

    def _validate(self,value):
        if not isinstance(value,self._data_type):
            raise TypeError("value must be {}".format(self._data_type.__name__))
        if not(self.min <= value <= self.max):
            raise ValueError("value must be in (min,max)")


class CharField(Field):
    """
    字符串类型的数据描述符
    """

    def __init__(self,*args,min_length= 0,max_length=256,regx='',**kwargs):
        """

        :param args:
        :param min_length:
        :param max_length:
        :param regx: 用于验证value是否匹配规则
        :param kwargs:
        """
        if not isinstance(min_length,int):
            raise TypeError('min_length must be Integer')
        if min_length < 0:
            raise ValueError('min_length must be lager 0')
        if not isinstance(max_length, int):
            raise TypeError('max_length must be Integer')
        if min_length > max_length :
            raise ValueError("must (min_length <= max_length)")

        self.min_lenght =min_length
        self.max_length = max_length
        self.regx = regx
        super(CharField, self).__init__(*args, **kwargs)

    def _validate(self,value):
        """
        value必须是字符串，同时长度在min_length和max_length之间，能和regx完全匹配
        :param value:
        :return:
        """
        if not isinstance(value,str):
            raise TypeError("value must be str")
        length = len(value)
        if not (self.min_lenght <= length <= self.max_length):
            raise ValueError("len(value) must be in (min_length,max_length)")
        if self.regx:
            if not re.fullmatch(self.regx,value):
                raise ValueError("vlaue can't fullmatch {}".format(self.regx))


class IntegerField(FloatField):
    _data_type = int


class Student:
    name = CharField(min_length=2,max_length=12)
    age = IntegerField(min=12,max=60)
    weight = FloatField(min=40,max=200)


    def __init__(self,name,age,weight):
        self.name = name
        self.age = age
        self.weight = weight


bob = Student('cuiddd',12,140)
bob.name = 'cui'
print(bob.weight)


