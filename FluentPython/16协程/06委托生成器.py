from collections import namedtuple

Result = namedtuple('Result','count average')
result = {}

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

def main():
    data ={
        'k1':[1,2,3,4,5,6,7,8],
        'k2':[3,4,2,54,7,8],
        'k3':[4,5,2,5,3,22,33,44,55]
    }

    for key,items in data.items():
        g = averager()
        next(g)
        for i in items:
            g.send(i)

        try :
            g.send(None)
        except StopIteration as e:
            temp = e.value
            result[key] =temp
    print(result)

if __name__ == "__main__":
    main()

    # {'k1': Result(count=8, average=4.5), 'k2': Result(count=6, average=13.0),
    # 'k3': Result(count=9, average=19.22222222222222)}


