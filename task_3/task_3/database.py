from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine=create_engine('postgresql://postgres:inferno@localhost/todo')

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
