from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserRegister(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str | None
    password: str
    password_repeat: str

class UserLogin(BaseModel):
    email : EmailStr
    password: str = Field(..., max_length=128)