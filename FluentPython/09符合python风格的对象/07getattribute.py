
class User1:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __getattribute__(self, item):
        print(item)
        return super().__getattribute__(item)

    def func(self):
        return 1234

u = User1('bob',2)

print(u.func())
# func
# 1234


class User:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __getattribute__(self, item):
        print(item)
        return 123

    def func(self):
        return 1234

u = User('bob',2)

print(u.func)
# func
# 123
print(u.age)
# age
# 123