from abc import abstractmethod,ABCMeta
import abc

class BaseDisk(metaclass=ABCMeta):

    def __init__(self):
        self._storage = ''
        self.__pt = 0

    @abstractmethod
    def write(self,value):
        self._storage += value

class WDDisk(BaseDisk):

    def write(self,value):
        super().write(value)
        print('WDDisk write {}'.format(value))
        print(self._BaseDisk__pt)

class WWDisk(WDDisk):

    def pt(self):
        print(self._BaseDisk__pt)
# b = WDDisk()
# b.write('123')
#
# w = WWDisk()
# w.pt()

a = '1233'
print(str(a))
a.encode()

from types import MappingProxyType
