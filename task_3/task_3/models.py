from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column ,ForeignKey,Integer,String,DateTime,Text
from sqlalchemy.sql import func
Base=declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False,unique=True)
    email=Column(String(80),nullable=False,unique=True)
    password=Column(String(150),nullable=False)
    todos = relationship("Todo", back_populates="owner",cascade="all, delete" )

    def __repr__(self):
        return f"<User {self.name}>"
    

class Todo(Base):
    __tablename__='todo'
    id=Column(Integer,primary_key=True)
    name=Column(String(20),nullable=False,unique=True)
    description=Column(Text,nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))

    owner = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<Todo {self.name}>"
    