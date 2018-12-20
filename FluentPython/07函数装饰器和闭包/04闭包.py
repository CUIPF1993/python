def make_averager():
    # series 是一个自由变量
    series = []
    def average(new_vlaue):
        series.append(new_vlaue)
        value = sum(series)/len(series)
        print(value)
    return average

aver = make_averager()
for i in range(10):
    aver(i)

# 0.0
# 0.5
# 1.0
# 1.5
# 2.0
# 2.5
# 3.0
# 3.5
# 4.0
# 4.5

# nonlocal 将值类型转换为自由变量
def make_averager():
    total = 0
    length =0
    def average(new_value):
        nonlocal total,length
        total += new_value
        length += 1
        value = total/length
        print(value)
    return average


aver = make_averager()
for i in range(20,30):
    aver(i)

# 20.0
# 20.5
# 21.0
# 21.5
# 22.0
# 22.5
# 23.0
# 23.5
# 24.0
# 24.5