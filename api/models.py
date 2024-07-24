from pydantic import BaseModel, confloat, EmailStr, field_validator, FieldValidationInfo, ValidationError
from typing import Union
import requests
import datetime
import uuid
import json

# url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v1.json'
#
# response = requests.get(url)
# data = response.json()

json_data = '''
{
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com",
    "is_active": true,
    "birth_date" : "2007-01-01"
}
'''


# define Pydantic model class
class Student(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool
    birth_date: datetime.date

    @field_validator('birth_date')
    def check_age_16(cls, value):
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) <
                                         (value.month, value.day))
        print('age is :', age)

        if age < 16:
            raise ValueError("Need to be older than 16 yrs")
        return value

    @field_validator('birth_date')
    def check_age_18(cls, value, info: FieldValidationInfo):
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) <
                                         (value.month, value.day))

        if age < 18:
            raise ValueError("Need to be older than 18 yrs")
        return value


data = json.loads(json_data)
model = Student.parse_obj(data)
print(model)
