from fastapi import APIRouter,HTTPException,Depends,status
from typing import List,Annotated
from sqlalchemy.orm import session
import schemas,models
from database import get_db
from auth.hashing import get_password_hash
from auth.tokens import authenticate_user,create_access_token
from auth.auth import get_current_user
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

setting=schemas.Setting()
router=APIRouter(
    
    tags=['User']
)

@router.post("/register/",response_model=schemas.UserCreate)
def register(user:schemas.UserCreate, db:session=Depends(get_db)):
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

@router.post("/token",response_model=schemas.Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:session=Depends(get_db)):

    """this function creates token for authentication."""
    user = authenticate_user(form_data.username,form_data.password,db)
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


@router.get("/users/me")
async def read_users_me(current_user:models.User = Depends(get_current_user)):
    """This function shows all the information of logged user.
    This is created for test case"""
    return current_user