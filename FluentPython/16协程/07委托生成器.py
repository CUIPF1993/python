from collections import namedtuple

Result = namedtuple('Result','count average')
result = {}

# 子生成器
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

def grouper(result,key):
    """
    等同于下面两句
   """
    result[key] = yield from averager()
    a = yield
    # while True:
    #     result[key] = yield from averager()




def main():
    data ={
        'k1':[1,2,3,4,5,6,7,8],
        'k2':[3,4,2,54,7,8],
        'k3':[4,5,2,5,3,22,33,44,55]
    }

    for key,items in data.items():
        g = grouper(result,key)
        next(g)
        for i in items:
            g.send(i)
        g.send(None)
        g.send(1)
        g.send(1)
        g.send(1)
    print(result)

###################################################################

def main1():
    data ={
        'k1':[1,2,3,4,5,6,7,8],
        'k2':[3,4,2,54,7,8],
        'k3':[4,5,2,5,3,22,33,44,55]
    }

    for key,items in data.items():
        g = grouper(result,key)
        next(g)
        for i in items:
            g.send(i)
        g.send(None)        # 把 None 传入group，导致当前的 averager 实例终止，也让 grouper 继续运行产生一个新的 averager 实例

        for i in items:     # 这里是一个新的 averager 实例
            g.send(i)
    print(result)

############################################################


if __name__ == "__main__":
    main()
    main1()

    # {'k1': Result(count=8, average=4.5), 'k2': Result(count=6, average=13.0),
    # 'k3': Result(count=9, average=19.22222222222222)}


