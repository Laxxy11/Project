from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine=create_engine('postgres://postgres:inferno@localhost/fastapi')

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
