from functools import wraps
from collections import defaultdict


def validate(*ty_args,**ty_kwargs):
    def decorate(func):
        @wraps(func)
        def inner(*args,**kwargs):
            if not(len(ty_args)==len(args)):
                raise ValueError("参数不匹配")

            for value,ty in zip(args,ty_args):
                if not isinstance(value,ty):
                    raise TypeError("value must be {}".format(ty.__name__))

            vali = {}
            # 获取以name_maxlength类似的关键字参数
            for key,value in kwargs.items():
                for ty_key,ty_value in ty_kwargs.items():
                    pattern = key+"_"
                    if ty_key.startswith(pattern):
                        vali[ty_key] = ty_value

            for key, value in kwargs.items():
                ty = ty_kwargs.get(key)
                if not isinstance(value,ty):
                    raise TypeError("{} must be {}".format(key, ty.__name__))
            # 验证带后缀的参数
            """
            vali = {'age_min': 12,
                    'age_max': 36, 
                    'name_minlength': 3,
                    'name_maxlength': 8}
                        
            遍历vali,从val_func_list中取出匹配的函数，进行验证
            """
            for key,pattern in vali.items():
                key,val_name = key.split("_")
                value = kwargs[key]
                for val in val_func_list:
                    if val.__name__ == val_name:
                        val(key,pattern,value)

            result = func(*args,**kwargs)
            return result
        return inner
    return decorate



# 定义一些通用的验证函数
val_func_list =[]

# 注册函数
def register(func):
    val_func_list.append(func)
    return func

@register
def minlength(key,length,value):
    if len(value)<length:
        raise ValueError("{} length must larger {}".format(key,length))

@register
def maxlength(key,length,value):
    if len(value)>length:
        raise ValueError("{} length must smaller {}".format(key,length))

@register
def min(key,num,value):
    if value < num:
        raise ValueError("{} must be larger {}".format(key,num))

@register
def max(key,num,value):
    if value > num:
        raise ValueError("{} must be smaller {}".format(key,num))






@validate(int,age= int,name=str,age_min=12,age_max=36,name_minlength=3,name_maxlength=8)
def fun(weight,age,name):
    pass

fun(5,age =12,name='cui')

