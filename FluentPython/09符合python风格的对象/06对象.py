import re
import copy
from abc import abstractmethod

class Field(object):
    __count =1

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

class BaseModel:
    def __init__(self,*args,**kwargs):
        cls = self.__class__
        mappings = dict()

        for key,value in cls.__dict__.items():
            if not key.startswith('__') and isinstance(value, Field):
                mappings[key] = value
        # 获取经过排序的字典对象
        length = len(mappings)
        order_field = sorted(mappings.items(),key=lambda item:item[1].count)
        self._order_field = copy.deepcopy(order_field)
        for i,value in enumerate(args):
            try:
                item = order_field.pop(0)
                key, field = item
                setattr(self, key, value)
            except IndexError:
                raise IndexError('args length must be shorted {}'.format(length))
        for key,field in order_field:
            setattr(self, key, kwargs.get(key))

        super().__init__()

    def __iter__(self):
        for key,field in self._order_field:
            yield field

    def __call__(self, *args, **kwargs):
        return [str(field) for field in self]



class User(BaseModel):
    name = CharField()
    nickname = CharField()
    password = CharField()
    class_name = CharField()
    teacher = CharField()
    teachers = CharField()


class BaseModeSerializer:

    class Meta:
        model = None
        fields = "__all__"

    def __init__(self,instance=None,data=None,many=False):
        cls = self.__class__
        if instance and not isinstance(instance,cls.Meta.model):
            raise TypeError("instance must be {}".format(cls.Meta.model.__name__))

        if instance and data:
            raise ValueError("instance and data just need one")
        self.instance = instance
        self.many = many
        self.data =data


    @property
    def dict(self):
        if self.many == False:
            result = self._serialization(instance=self.instance)
        else:
            result =[]
            result.append(self._serialization(instance=self.instance))
        return result

    def _serialization(self,instance):
        pass


    @property
    def models(self):
        if not isinstance(self.data,list):
            result = self._deserialization(self.data)
        else:
            result = []
            result.append(self._serialization(self.data))
        return self

    def _deserialization(self,data):
        cls = self.__class__
        model_cls = cls.Meta.model
        order_field =[]
        for key,field in model_cls.__dict__.items():
            if not key.startswith('__') and isinstance(field,Field):
                order_field.append((key,field))
        model = model_cls(**data)


        return model





class UserSerializer(BaseModeSerializer):
    class Meta:
        model = User




u = User(name='cc',nickname='jackchen',class_name='11',password = '12345',teacher='jag',teachers='jag')
data = {'name':'cc','nickname':'jackchen','class_name':'11','password':'12345','teacher':'jag','teachers':'jag'}
s = UserSerializer(data=data)
m = s.models
print(type(m))













# b = BaseModeForm()
# cls = b.__class__
# print(cls.Meta.model)



# u = User('cc',nickname='jackchen',class_name='11',password = '12345',teacher='jag',teachers='jag')
# print(u.name)
#
# for field in u:
#     print(field)

