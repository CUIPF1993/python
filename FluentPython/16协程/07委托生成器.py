from collections import namedtuple

Result = namedtuple('Result','count average')
result = {}

"""
委派生成器在yield from 表达式处暂停时，调用方可以直接把数据发送给子生成器，子生成器再把产出的值发给调用方，
子生成器返回后，解释器会抛出 StopIteration 异常，并把返回值加到异常对象上，此时委派生成器恢复正常。

"""

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

# 委托生成器
def grouper(result,key):
    """
    等同于下面两句
   """
    # result[key] = yield from averager()
    # a = yield
    while True:
        result[key] = yield from averager()



# 客户端代码，即调用方
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
        for i in items:
            g.send(i)

    print(result)

############################################################
def grouper2(result,key):
    """
    等同于下面两句
   """
    result[key] = yield from averager()

def main2():
    data ={
        'k1':[1,2,3,4,5,6,7,8],
        'k2':[3,4,2,54,7,8],
        'k3':[4,5,2,5,3,22,33,44,55]
    }

    for key,items in data.items():
        g = grouper2(result, key)
        next(g)
        for i in items:
            g.send(i)
        """
        1.子生成器可以执行return语句，返回一个值，而返回的值会成为yield表达式的值。
        2.子生成器退出时，子生成器中的retrun expr 会触发StopIteration异常。
        3.yield from 表达式的值是子生成器终止时传给StopIteration异常的第一个参数。
        
        """
        try :
            g.send(None)
        except StopIteration as e:
            print("e ------->",e.value)
    print(result)


############################################
def main3():
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
        """
        调用throw()方法时抛出StopIteration异常，委派生成器回复运行，StopIteration之外的异常会向上冒泡，传给委派生成器。
        """
        g.throw(StopIteration)

    print(result)
if __name__ == "__main__":
    main()
    # {'k1': Result(count=8, average=4.5), 'k2': Result(count=6, average=13.0),
    #  'k3': Result(count=9, average=19.22222222222222)}


    main1()
    # {'k1': Result(count=8, average=4.5), 'k2': Result(count=6, average=13.0),
    #  'k3': Result(count=9, average=19.22222222222222)}


    main2()
    # e - ------> None
    # e - ------> None
    # e - ------> None
    # {'k1': Result(count=8, average=4.5), 'k2': Result(count=6, average=13.0),
    #  'k3': Result(count=9, average=19.22222222222222)}

    main3()
    # {'k1': None, 'k2': None, 'k3': None}


