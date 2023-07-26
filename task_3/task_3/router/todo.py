from typing import List
from fastapi import APIRouter,HTTPException,Depends
from database import get_db
import schemas,models
from auth.auth import get_current_user
from sqlalchemy.orm import Session



router=APIRouter(prefix="/todo",
    tags=['TODO'])


@router.get("/",status_code=200,response_model=List[schemas.Todo])
async def read_all_todo(user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_todos=db.query(models.Todo).filter(models.Todo.user_id==user.id).all()
    db_json=[db_todo for db_todo in db_todos]
    return db_json

@router.get("/{todo_id}",response_model=schemas.Todo)
async def read_todo(todo_id:int ,db:Session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    if db is None:
        raise HTTPException(status_code=400, detail="No such task")
    return db_todo

@router.post("/",response_model=schemas.Todo)
async def create_todo(todo:schemas.CreateTodo,user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
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

@router.delete("/{todo_name}",response_model=schemas.Todo)
async def remove(todo_name:str,user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.name==todo_name,models.Todo.user_id==user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=400,detail="No such task is present")
    db.delete(db_todo)
    db.commit()
    return db_todo

@router.put("/{todo_id}",response_model=schemas.Todo)
def update_todo(todo_id: int, todo:schemas.CreateTodo,user:models.User=Depends(get_current_user), db:Session = Depends(get_db)):
        db_todo = db.query(models.Todo).filter(models.Todo.id==todo_id,models.Todo.user_id==user.id).first()
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db_todo.name = todo.name
        db_todo.description=todo.description
        db.commit()
        return db_todo