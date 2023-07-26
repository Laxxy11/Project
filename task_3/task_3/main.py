from fastapi import FastAPI
from router import todo,user


app=FastAPI()
app.include_router(todo.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
