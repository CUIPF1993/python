def gen():
    for i in range(3):
        yield i
    for i in range(3,6):
        yield i

print(list(gen()))
# [0, 1, 2, 3, 4, 5]

# g = gen()
# for i in range(7):
#     next(g)


def gen():
    yield from (range(3))
    yield from (range(3,6))

print(list(gen()))
# [0, 1, 2, 3, 4, 5]

"""
yield from x   表达式对 x对象 所作的第一件事就是，调用iter(x)，从中获取迭代器。因此 x 可以是任何可迭代对象


yield from 的真正作用：
yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样两者可以直接发送和产出值，
还可以直接传入异常，而不用在位于中间的协程中添加大量的异常的样板代码。有了这个结构，协程可以通过以前不可能的方式委托职责。
"""
# g = gen()
# for i in range(7):
#     next(g)