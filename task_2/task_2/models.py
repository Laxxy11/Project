from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,String,DateTime,Integer

Base=declarative_base()

class User(Base):
    __tablename__="users"
    id=Column(Integer(),primary_key=True)
    name=Column(String(),nullable=False)
    email=Column(String(),unique=True,nullable=False)
    password=Column(String(),nullable=False)
