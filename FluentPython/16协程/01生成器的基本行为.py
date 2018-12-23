def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(next(g))
print(next(g))
print(next(g))

# 1
# 2
# 3
print(10*"*")

g = gen()
print(g.send(None))
print(g.send(None))
print(g.send(None))

# 1
# 2
# 3
print(10*"*")

def gen():
    print("gen start")
    a = yield 1
    print("a = {}".format(a))
    b = yield 2
    print("b = {}".format(b))
    c = yield 3
    print("c = {}".format(c))

g = gen()
print(g.send(None))
# gen start
# 1
print(g.send(11))
# a = 11
# 2
print(g.send(22))
# b = 22
# 3
print(g.send(33))
# c = 33
# StopIteration