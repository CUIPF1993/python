from abc import abstractmethod
import abc



class BaseDisk(metaclass = abc.ABCMeta):

    def __init__(self,brand,size,price,hardware_connectivity,file_system):
        """

        :param brand:
        :param size:
        :param price:
        :param hardware_connectivity:
        :param file_system:
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
        pass

    @abstractmethod
    def read(self,bytes_size = 1024):
        pass

    def seek(self,value):
        pass


class WDDisk(BaseDisk):
    def __init__(self,*args,**kwargs):
        super().__init__('WD',*args,**kwargs)

    def write(self,value):
        print(self.brand + 'write {}'.format(value))
        self._storage += ''

    def read(self,bytes_size = 1024):
        pass


class SeagateDisk(BaseDisk):
    def __init__(self, *args, **kwargs):
        super().__init__('Seagate', *args, **kwargs)

    def write(self, value):
        print(self.brand + 'write {}'.format(value))

    def read(self, bytes_size=1024):
        pass





