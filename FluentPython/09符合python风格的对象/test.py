a = [1,2,3,4,5]
print(a)
print(sorted(a))
print(sorted(a,key=lambda x:-x))

def add(x,y,z=0):
    return x+y+z

# error :add(3,x=1,z=4)


# for i in range(4):
#     print(a.pop(0))


class Person:
    __count =0

    def __init__(self):
        cls = self.__class__
        cls.__count +=1

    @property
    def count(self):
        return self.__count

class School:
    a = Person()
    b = Person()


a = Person()
b = Person()

卡是 = 1244
print(卡是)


print('GHJJ'.lower())
