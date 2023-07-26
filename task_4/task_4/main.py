from fastapi import FastAPI
from fastapi import Depends,HTTPException,status
from typing import List,Annotated

from fastapi.encoders import jsonable_encoder
import schemas ,models
from auth import verify_password,get_password_hash,create_access_token,jwt,JWTError,setting
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer,HTTPBearer
from database import sessionlocal
from datetime import datetime,timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username:str,password:str,db:Session=Depends(get_db)):
    """This function authenticate the users by comparing database value and the OAuth2PasswordRequestForm values . """
    user=db.query(models.User).filter(models.User.username==username).first()
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate" :"Bearer"},)
    try:
        payload=jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        name:str=payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data=schemas.TokenData(username=name)
    except JWTError:
        raise credentials_exception
    user=db.query(models.User).filter(models.User.username==token_data.username).first()
    if user is None:
        raise credentials_exception
    return user




app=FastAPI()

#user registration
@app.post("/register/",response_model=schemas.UserCreate,tags=["user"])
async def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    """Api endpoint to create new users."""
    db_user=db.query(models.User).filter(models.User.username==user.username).first()
    db_email=db.query(models.User).filter(models.User.email==user.email).first()
    if db_user or db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    hash_password=get_password_hash(user.password)
    new_user=models.User(username=user.username,password=hash_password,email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token/",response_model=schemas.Token,tags=["user"])
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):

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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/blogs/",status_code=status.HTTP_200_OK,response_model=List[schemas.Blog],tags=["Blog"])
async def read_all_blogs(user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
   db_blogs=db.query(models.Blog).filter(models.Blog.user_id==user.id).all()
   print("--------------------------------------------------")
   print(db_blogs)
   print(type(db_blogs))
   blog_list=[db_blog for db_blog in db_blogs]
   return blog_list

@app.get("/blogs/{blog_id}/",status_code=status.HTTP_200_OK,response_model=schemas.Blog,tags=["Blog"])
async def read_blog(blog_id:int,db:Session=Depends(get_db),user:models.User=Depends(get_current_user)):
    db_blog=db.query(models.Blog).filter(models.Blog.id==blog_id,models.Blog.user_id==user.id).first()
    if db_blog is None:
        raise HTTPException(status_code=400, detail="No such task")
    return db_blog 

@app.post("/blogs/",status_code=status.HTTP_201_CREATED,response_model=schemas.Blog,tags=["Blog"])
async def create_blog(blog:schemas.Post_Blog,db:Session=Depends(get_db),user:models.User=Depends(get_current_user)):
    db_blog=db.query(models.Blog).filter(models.Blog.title==blog.title).first()
    if db_blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Todo already exist")
    new_blog=models.Blog(title=blog.title,
                         content=blog.content,
                         user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{blog_title}/",response_model=schemas.Blog,tags=["Blog"])
async def remove(blog_title:str,user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_blog=db.query(models.Blog).filter(models.Blog.title==blog_title,models.Blog.user_id==user.id).first()
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No such Blog is present")
    db.delete(db_blog)
    db.commit()
    return db_blog

@app.put("/blogs/{blog_name}/",status_code=status.HTTP_201_CREATED,response_model=schemas.Blog,tags=["Blog"])
async def change_blog(blog_name:str,blog:schemas.Post_Blog,db:Session=Depends(get_db),user:models.User=Depends(get_current_user)):
    db_blog = db.query(models.Blog).filter(models.Blog.title==blog_name,models.Blog.user_id==user.id).first()
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db_blog.title = blog.title
    db_blog.content=blog.content
    db.commit()
    return db_blog



@app.get("/users/me")
async def read_users_me(current_user:models.User = Depends(get_current_user)):
    """This function shows all the information of logged user.
    This is created for test case"""

    #user_details=jsonable_encoder(current_user)
    #return user_details["name"]
    return current_user