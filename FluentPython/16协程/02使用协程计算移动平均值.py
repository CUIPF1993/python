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
next(aver)      #预激协程
for i in range(0,30,3):
    print(aver.send(i))

# 0.0
# 1.5
# 3.0
# 4.5
# 6.0
# 7.5
# 9.0
# 10.5
# 12.0
# 13.5

from inspect import getgeneratorstate

aver = averager()
print(getgeneratorstate(aver))      # 查看生成器状态
next(aver)
print(getgeneratorstate(aver))
for i in range(0,30,3):
    print(aver.send(i))
aver.close()
print(getgeneratorstate(aver))