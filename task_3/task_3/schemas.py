import datetime
from pydantic import BaseModel,EmailStr

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Todo(BaseModel):
    name:str
    description:str
    user_id: int

    class Config:
        orm_mode = True

class CreateTodo(BaseModel):
    name:str
    description:str



class User(BaseModel):
    name:str
    email:EmailStr
    todos:list[Todo]=[]

    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None

#for loading a settings or config class from environment variables or secrets files.
class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')