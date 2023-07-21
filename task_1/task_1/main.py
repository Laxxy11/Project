from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from starlette.responses import JSONResponse
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from dotenv import load_dotenv
import os


#validation of email type
class EmailSchema(BaseModel):
    email:List[EmailStr]



class Setting(BaseSettings):
    """ This class is used for validation of .env settings parameters.Similarly we used pydantic setting to read environment variables."""
    MAIL_USERNAME : str
    MAIL_PASSWORD: str
    MAIL_SERVER:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_FROM_NAME:str =""
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS:bool=True
    VALIDATE_CERTS:bool=True

    # class Config:
    #   env_file='.env'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')



#using dotenv lib to read from .env file


# load_dotenv()
# config=ConnectionConfig(
#     MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
#     MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
#     MAIL_FROM=os.getenv("MAIL_FROM"),
#     MAIL_SERVER=os.getenv("MAIL_SERVER"),
#     MAIL_PORT=int(os.getenv("MAIL_PORT")),
#     MAIL_FROM_NAME=os.getenv(""),
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )
#settings = Setting(_env_file='.env', _env_file_encoding='utf-8')

settings=Setting() 

#print(settings.MAIL_USERNAME)

config=ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True)


app=FastAPI()

@app.post("/email")
async def send_mail(email:EmailSchema)->JSONResponse:
    html=""" <p> This is test mail using fastapi-mail</p>"""

    message=MessageSchema(
        subject="sending mail using fastapi-mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html)
    
    fm=FastMail(config)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message":"mail successfully send"})

