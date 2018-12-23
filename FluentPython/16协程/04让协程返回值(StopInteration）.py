from collections import namedtuple

Result = namedtuple('Result','count average')


def averager():
    total = 0
    count =0
    average = None
    while True:
        num = yield
        if num == None:
            break
        total +=num
        count +=1
        average = total/count
    return Result(count,average)

aver =averager()
next(aver)

for i in range(0,30,3):
    aver.send(i)

try:
    aver.send(None)
except StopIteration as e:
    result = e.value
    print(result)
    # Result(count=10, average=13.5)
