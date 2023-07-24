import datetime
from pydantic import BaseModel
from typing import List
from pydantic import BaseModel

class Todo(BaseModel):
    name:str
    description:str
    user_id: int

    class Config:
        orm_mode = True

class CreateTodo(BaseModel):
    name:str
    description:str
    
class TodoinDB(BaseModel):
    name:str
    description:str
    user_id: int
    created_time: datetime.datetime

class User(BaseModel):
    name:str
    email:str
    todos:list[Todo]=[]

    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
class Userlogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None