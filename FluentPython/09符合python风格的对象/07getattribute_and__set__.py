import re

class Field(object):
    __count =1

    def __init__(self,*args,**kwargs):
        cls = self.__class__
        prefix = cls.__name__
        self.name = '{prefix}__{count}'.format(prefix=prefix,count=cls.__count)
        cls.__count+=1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self._validate(value)
        instance.__dict__[self.name] =value


    def _validate(self,value):
        raise NotImplementedError('未实现self.validate')


class CharField(Field):
    def __init__(self,min_length:int=0,max_length:int=128,regx:str='',*args,**kwargs):
        super().__init__(*args,**kwargs)
        if not isinstance(min_length,int):
            raise TypeError("min_length must be int")
        if not isinstance(max_length, int):
            raise TypeError("max_length must be int")
        self.min_length = min_length
        self.max_length = max_length
        self.regx = regx

    def _validate(self,value):
        if not isinstance(value,str):
            raise ValueError('value must be str')
        length = len(value)
        if self.max_length and length > self.max_length:
            raise ValueError("value length must be shorter than max_length")
        if self.min_length and length < self.min_length:
            raise ValueError("value length must be larger than min_length")

        if self.regx:
            if not re.fullmatch(self.regx,value):
                raise ValueError("vlaue can't fullmatch {}".format(self.regx))


class User:
    name = CharField()

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __getattribute__(self, item):
        print(item)
        return super().__getattribute__(item)

    def func(self):
        return 1234

u = User('bob',2)
# __dict__