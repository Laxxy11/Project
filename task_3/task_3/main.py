from fastapi import FastAPI
from fastapi import FastAPI,Depends,HTTPException,status
import models,schemas
from datetime import datetime, timedelta
from typing import Annotated,List
from sqlalchemy.orm import session
from database import sessionlocal,engine
from hashing import verify_password,get_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError,jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app=FastAPI()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



def authenticate_user(username: str, password: str,db:session=Depends(get_db)):
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:session=Depends(get_db)):
    """to get user information from payload of jwt and in this case username  """

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate" :"Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        name:str=payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data=schemas.TokenData(name=name)
    except JWTError:
        raise credentials_exception
    print(token_data.name)
    user=db.query(models.User).filter(models.User.name==token_data.name).first()
    if user is None:
        raise credentials_exception
    print("--------------------------------------------------------")
    print(type(user))
    print(user.id)
    return user



@app.get("/todo",status_code=200,response_model=List[schemas.Todo])
async def read_all_todo(user:models.User=Depends(get_current_user),db:session=Depends(get_db)):
    print("-----------------------------------------------------------------")
    print(user.id)
    db_todos=db.query(models.Todo).filter(models.Todo.user_id==user.id).all()
    db_json=[db_todo for db_todo in db_todos]
    return db_json

@app.get("/todo/{todo_id}",response_model=schemas.Todo)
async def read_todo(todo_id:int ,db:session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    if db is None:
        raise HTTPException(status_code=400, detail="No such task")
    return db_todo

@app.post("/todo/",response_model=schemas.Todo)
async def create_todo(todo:schemas.CreateTodo,user:models.User=Depends(get_current_user),db:session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.name==todo.name).first()
    if db_todo:
        raise HTTPException(status_code=400,detail="Todo already exist")
    new_todo=models.Todo(
        name=todo.name,
        description=todo.description,
        user_id=user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.delete("/todo/{todo_name}",response_model=schemas.Todo)
async def remove(todo_name:str,user:models.User=Depends(get_current_user),db:session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.name==todo_name,models.Todo.user_id==user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=400,detail="No such task is present")
    db.delete(db_todo)
    db.commit()
    return db_todo

@app.put("/todo/{todo_id}",response_model=schemas.Todo)
def update_todo(todo_id: int, todo:schemas.CreateTodo,user:models.User=Depends(get_current_user), db:session = Depends(get_db)):
        db_todo = db.query(models.Todo).filter(models.Todo.id==todo_id,models.Todo.user_id==user.id).first()
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db_todo.name = todo.name
        db_todo.description=todo.description
        db.commit()
        return db_todo



#user registration
@app.post("/register/",response_model=schemas.UserCreate)
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

@app.post("/token",response_model=schemas.Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:session=Depends(get_db)):

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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user:models.User = Depends(get_current_user)):
    """This function shows all the information of logged user.
    This is created for test case"""

    #user_details=jsonable_encoder(current_user)
    #return user_details["name"]
    return current_user