from fields import Field

class BaseModeSerializer:

    class Meta:
        model = None
        fields = "__all__"

    def __init__(self,instance=None,data=None,many=False):
        cls = self.__class__
        if instance and not isinstance(instance,cls.Meta.model):
            raise TypeError("instance must be {}".format(cls.Meta.model.__name__))

        if instance and data:
            raise ValueError("instance and data just need one")
        self.instance = instance
        self.many = many
        self.data =data


    @property
    def dict(self):
        if self.many == False:
            result = self._serialization(instance=self.instance)
        else:
            result =[]
            result.append(self._serialization(instance=self.instance))
        return result

    def _serialization(self,instance):
        pass


    @property
    def models(self):
        if not isinstance(self.data,list):
            result = self._deserialization(self.data)
        else:
            result = []
            result.append(self._serialization(self.data))
        return self

    def _deserialization(self,data):
        cls = self.__class__
        model_cls = cls.Meta.model
        order_field =[]
        for key,field in model_cls.__dict__.items():
            if not key.startswith('__') and isinstance(field,Field):
                order_field.append((key,field))
        model = model_cls(**data)


        return model









