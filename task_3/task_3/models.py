from sqlalchemy.orm import declarative_base
from sqlalchemy import Column ,ForeignKey,Integer,String

class User(Base):
    __tablename__="users"