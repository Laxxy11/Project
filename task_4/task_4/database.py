from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine=create_engine('postgresql://postgres:inferno@localhost/blog')
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)