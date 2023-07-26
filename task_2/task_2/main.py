from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from database import engine,sessionlocal
from jwt_auth import verify_password,get_password_hash
from fastapi.encoders import jsonable_encoder
import models,schemas
from schemas import Setting
from sqlalchemy.orm import Session
from jose import JWTError,jwt
from datetime import datetime,timedelta
from typing import Annotated



models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting=Setting()
auth=HTTPBearer()



def get_db():
    """this function makes new session for each request"""
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str,db:Session=Depends(get_db)):
    """"this function authenticate the users by comparing database value and the OAuth2PasswordRequestForm values """
    user = db.query(models.User).filter(models.User.name==username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    """"to create jwt token for name"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:Session=Depends(get_db)):
    """to get user information from payload of jwt and in this case username  """

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate" :"Bearer"},
    )
    try:
        payload=jwt.decode(token,setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data=schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    print(token_data.username)
    user=db.query(models.User).filter(models.User.name==token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

#async def get_current_user_HTTPBearer(token:Annotated[str,Depends(auth)],db:Session=Depends(get_db)):
async def get_current_user_HttpBearer(request:HTTPAuthorizationCredentials=Depends(auth),db:Session=Depends(get_db)):
    token=request.credentials
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate" :"Bearer"},
    )
    try:
        payload=jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data=schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user=db.query(models.User).filter(models.User.name==token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


app=FastAPI()


#user registration
@app.post("/register/",response_model=schemas.UserCreate)
def register(user:schemas.UserCreate, db:Session=Depends(get_db)):
    """"Api end point to register new users"""
    
    db_user=db.query(models.User).filter(models.User.name==user.name).all()
    db_email=db.query(models.User).filter(models.User.email==user.email).first()
    if db_user or db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    hash_password=get_password_hash(user.password)
    new_user=models.User(name=user.name,email=user.email,password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token",response_model=schemas.Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):

    """this function creates token for authentication."""
    user = authenticate_user(form_data.username,form_data.password,db)
    print("---------------------------------------------------------------------------------------------------")
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user:models.User = Depends(get_current_user_HttpBearer)):

    #user_details=jsonable_encoder(current_user)
    #return user_details["name"]
    return current_user