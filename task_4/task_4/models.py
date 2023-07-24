from sqlalchemy import Column,Text,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base,relationship,backref
from sqlalchemy.sql import func
from datetime import datetime



Base=declarative_base()

class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    content=Column(Text)
    created_time=Column(DateTime(timezone=True), server_default=func.now())
    updated_time=Column(DateTime(timezone=True),onupdate=func.now())
    user_id=Column(Integer,ForeignKey("users.id"))
    users=relationship("User",backref=backref("blogs",cascade="all,delete"))

    def __repr__(self):
        return f"<Blog {self.title}>"


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    def __repr__(self):
        return f"<User {self.name}>"
