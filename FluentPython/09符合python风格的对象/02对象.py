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


# class CharField(Field):
#     """
#     字符串类型的数据描述符
#     """
#
#     def __init__(self,*args,min_length= 0,max_length=256,regx='',**kwargs):
#         """
#
#         :param args:
#         :param min_length:
#         :param max_length:
#         :param regx: 用于验证value是否匹配规则
#         :param kwargs:
#         """
#         if not isinstance(min_length,int):
#             raise TypeError('min_length must be Integer')
#         if min_length < 0:
#             raise ValueError('min_length must be lager 0')
#         if not isinstance(max_length, int):
#             raise TypeError('max_length must be Integer')
#         if min_length > max_length :
#             raise ValueError("must (min_length <= max_length)")
#
#         self.min_lenght =min_length
#         self.max_length = max_length
#         self.regx = regx
#         super(CharField, self).__init__(*args, **kwargs)
#
#     def _validate(self,value):
#         """
#         value必须是字符串，同时长度在min_length和max_length之间，能和regx完全匹配
#         :param value:
#         :return:
#         """
#         if not isinstance(value,str):
#             raise TypeError("value must be str")
#         length = len(value)
#         if not (self.min_lenght <= length <= self.max_length):
#             raise ValueError("len(value) must be in (min_length,max_length)")
#         if self.regx:
#             if not re.fullmatch(self.regx,value):
#                 raise ValueError("vlaue can't fullmatch {}".format(self.regx))


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


class Metaclass(type):

    def __new__(cls, name,bases,attrs):
        print('a')
        mappings = dict()
        for key,value in attrs.items():
            # print(key,'------>' ,value)
            if not key.startswith('_') and isinstance(value, Field):

                mappings[key] = value

        # for k in mappings.keys():
        #     attrs.pop(k)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        return type.__new__(cls, name, bases, attrs)

class Person(metaclass=Metaclass):

    name = CharField()

    def __init__(self,*args,**kwargs):
        for k,v in self.__mappings__.items():
           setattr(self,k,kwargs.get(k))
        super().__init__()



p = Person(3,4,name=123)
print(p.__dict__)
print(Person.__class__)
print(p.name)