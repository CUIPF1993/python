# _*_coding:utf-8_*_
import math


class Vector2d(object):

    def __init__(self,x,y):
        self.__x = x
        self.__y =y

    @property
    def X(self):
        return self.__x

    @property
    def Y(self):
        return self.__y

    def __repr__(self):
        return 'Vector({},{})'.format(self.X,self.Y)

    def __str__(self):
        return str((self.X,self.Y))

    def __hash__(self):
        return hash(self.X)^hash(self.Y)

    def __abs__(self):
        return math.hypot(self.X,self.Y)

    def __add__(self, other):
        new = Vector2d(self.X+other.X,self.Y+other.Y)
        return new

    def __sub__(self, other):
        new = Vector2d(self.X-other.X,self.Y-other.Y)
        return new

    def angle(self):
        return math.atan2(self.Y,self.X)

    @classmethod
    def abs_vector(cls,x,y):
        x ,y = abs(x),abs(y)
        return cls(x,y)

v1 = Vector2d(3,4)
v2 = Vector2d(4,5)

print(v1+v2)

