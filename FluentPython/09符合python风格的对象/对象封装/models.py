import copy
from fields import Field


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



