from pydantic import BaseModel,EmailStr
import datetime
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional,List

#this schema is used for creating new user
class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

#for response 
class Blog(BaseModel):
    title:str 
    content:str
    user_id:int
   

#this schema is used for creating new blog
class Post_Blog(BaseModel):
    title:str
    content:str

#this schema is used for reading blog
class Read_Blog(BaseModel):
    title:str
    content:str
    created_time:Optional[str]
    updated_time:Optional[str]
    user_id: int

    class Config:
        orm_mode=True

class User(BaseModel):
    name:str
    email:str
    blogs:List[Read_Blog]=[]

    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

#for loading a settings or config class from environment variables or secrets files.
class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')