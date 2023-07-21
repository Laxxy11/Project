from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
class User(BaseModel):
    name:str
    email:str
    password:str

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
    username: str | None = None


class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')