class BaseResponse:
    def __init__(self):
        self.code = 200
        self.msg =''
        self.data ={}

    @property
    def dict(self):
        return self.__dict__