from functools import wraps

def priming(func):
    """

    :param func:
    :return:
    """
    wraps((func))
    def inner(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return inner


@priming
def averager():
    total = 0
    count =0
    average = 0
    while True:
        num = yield average
        total +=num
        count +=1
        average = total/count

aver = averager()
for i in range(10,30,3):
    print(aver.send(i))
