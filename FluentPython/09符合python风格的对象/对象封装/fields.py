import re
from abc import abstractmethod

class Field(object):
    __count =1
    type_code = None

    def __init__(self,label = None,help_text=None,**kwargs):
        cls = self.__class__
        prefix = cls.__name__
        self.__count = cls.__count
        self.name = '{prefix}__{count}'.format(prefix=prefix,count=cls.__count)

        self.label = label
        self.help_text = help_text

        cls.__count+=1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self._validate(value)
        instance.__dict__[self.name] =value

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def _validate(self,value):
        raise NotImplementedError('please implement self._validate')

    @property
    def count(self):
        return self.__count


class CharField(Field):
    type_code = str

    def __init__(self,min_length:int=0,max_length:int=128,regx:str='',**kwargs):
        super().__init__(**kwargs)
        if not isinstance(min_length,int):
            raise TypeError("min_length must be int")
        if not isinstance(max_length, int):
            raise TypeError("max_length must be int")
        self.min_length = min_length
        self.max_length = max_length
        self.regx = regx

        self.classes = ""
        if kwargs.get('classes'):
            self.classes = kwargs.get('classes')

        self._html = '<input id="{id}" name="{name}" class="{classes}" value="" maxlength="{maxlength}" autocomplete="off">'

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


    def __str__(self):
        return self._html.format(id =self.name,name = self.name,classes=self.classes,maxlength = self.max_length)


class IntegerField(Field):
    type_code = int

    def __init__(self,**kwargs):
        super().__init__(**kwargs)


    def _validate(self,value):
        cls = self.__class__
        if not isinstance(value,cls.type_code):
            raise TypeError('value must be {}'.format(cls.type_code.__name__))



class Float(IntegerField):
    type_code = float


class BoolField(IntegerField):
    type_code = bool

