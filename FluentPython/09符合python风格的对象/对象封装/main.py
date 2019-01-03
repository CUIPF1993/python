from fields import CharField
from models import BaseModel
from modelserializer import BaseModeSerializer

if __name__ == "__main__":
    class User(BaseModel):
        name = CharField()
        nickname = CharField()
        password = CharField()
        class_name = CharField()
        teacher = CharField()
        teachers = CharField()


    class UserSerializer(BaseModeSerializer):
        class Meta:
            model = User




    u = User(name='cc',nickname='jackchen',class_name='11',password = '12345',teacher='jag',teachers='jag')
    data = {'name':'cc','nickname':'jackchen','class_name':'11','password':'12345','teacher':'jag','teachers':'jag'}
    s = UserSerializer(data=data)
    m = s.models
    print(type(m))
