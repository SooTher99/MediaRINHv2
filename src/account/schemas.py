import datetime

from pydantic import BaseModel, EmailStr, Field, validator, FilePath
from src.types import constr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRegister(BaseModel):
    email: EmailStr
    first_name: constr(strip_whitespace=True, max_length=64)
    last_name: None | constr(strip_whitespace=True, max_length=64)
    password: constr(strip_whitespace=True, min_length=8, max_length=256)
    password_repeat: constr(strip_whitespace=True, min_length=8, max_length=256)

    @validator('password_repeat')
    def check_passwords_match(cls, password_repeat: str, values: dict):
        password = values.get('password')
        if password is not None and password_repeat is not None and password != password_repeat:
            raise ValueError('passwords do not match')
        return password

    class Config:
        schema_extra = {
            'example': {
                'email': 'SomeEmail@gmail.com',
                'first_name': 'Vladimir',
                'last_name': 'Abu_bandit',
                'password': 'Vikusya007',
                'password_repeat': 'Vikusya007'
            }
        }


class UserSuccessCreate(BaseModel):
    email: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'Вы успешно зарегистрировались, вам отправлено письмо для подтверждения почты.'
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)


class UserPersonArea(BaseModel):
    email: EmailStr
    first_name: constr(strip_whitespace=True, max_length=64)
    last_name: None | constr(strip_whitespace=True, max_length=64)
    date_joined: datetime.datetime
    post_agreement: bool
    avatar: None | FilePath

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'email': 'SomeEmail@gmail.com',
                'first_name': 'Vladimir',
                'last_name': 'Abu_bandit',
                'date_joined': '2023.05.19T22:13',
                'avatar': 'media/avatar/3fdsd1234fsdf123.png',
            }
        }