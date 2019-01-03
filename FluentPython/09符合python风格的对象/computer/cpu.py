from abc import abstractmethod
import abc
import time

class BaseCPU(metaclass=abc.ABCMeta):
    def __init__(self,brand,processor,processor_count,computer_memory_type):
        self.brand = brand
        self.processor = processor
        self.processor_count = processor_count
        self.computer_memory_type = computer_memory_type

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class IntelCPU(BaseCPU):
    def __init__(self,*args,**kwargs):
        super().__init__('intel',*args,**kwargs)

    def run(self):
        print(self.brand + 'is running')


    def stop(self):
        print(self.brand + 'stop')

class AMD(BaseCPU):
    def __init__(self, *args, **kwargs):
        super().__init__('intel', *args, **kwargs)

    def run(self):
        print(self.brand + 'is running running running ')

    def stop(self):
        print(self.brand + 'stop stop stop')


