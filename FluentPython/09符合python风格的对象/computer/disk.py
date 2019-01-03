from abc import abstractmethod
import abc



class BaseDisk(metaclass = abc.ABCMeta):

    def __init__(self,brand,size,price,hardware_connectivity,file_system):
        """

        :param brand:厂商
        :param size:存储容量
        :param price:价格
        :param hardware_connectivity:接口
        :param file_system:文件系统类型
        """
        self.brand = brand
        self.size = size
        self.price = price
        self.hardware_connectivity = hardware_connectivity
        self.file_system = file_system
        self._storage = ''
        self._pt = 0

    @abstractmethod
    def write(self,value):
        try:
            value = str(value)
            self._storage += value
        except:
            raise TypeError('must be str or str(value)')

    @abstractmethod
    def read(self,bytes_size = 1):
        head, tail = self._pt, self._pt + bytes_size
        if tail > len(self._storage):
            tail = len(self._storage)
        result = self._storage[head:tail]
        self._pt = tail
        if self._pt == len(self._storage):
            self._pt = 0

    def seek(self,pt):
        if pt > len(self._storage):
            raise ValueError('pt need smaller than {}'.format(len(self._storage)-1))
        self._pt = pt


class WDDisk(BaseDisk):
    def __init__(self,*args,**kwargs):
        super().__init__('WD',*args,**kwargs)

    def write(self,value):
        super().write(value)
        print(self.brand + 'write {}'.format(value))

    def read(self,bytes_size = 1):
        super().read(bytes_size)


class SeagateDisk(BaseDisk):
    def __init__(self, *args, **kwargs):
        super().__init__('Seagate', *args, **kwargs)

    def write(self, value):
        print(self.brand + 'write {}'.format(value))

    def read(self, bytes_size=1):
        pass





