from functools import wraps
from collections import defaultdict
import re

def validate(*ty_args,**ty_kwargs):
    def decorate(func):
        @wraps(func)
        def inner(*args,**kwargs):
            if not(len(ty_args)==len(args) and len(ty_kwargs)==len(kwargs)):
                raise ValueError("参数不匹配")

            for value,ty in zip(args,ty_args):
                if not isinstance(value,ty):
                    raise TypeError("value must be {}".format(ty.__name__))

            for key,ty in ty_kwargs.items():
                if not isinstance(kwargs[key],ty):
                    raise TypeError("{} must be {}".format(key,ty.__name__))
            result = func(*args,**kwargs)
            return result
        return inner
    return decorate

@validate(int,int)
def add(x,y):
    return x+y


