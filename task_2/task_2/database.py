from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine('postgresql://postgres:inferno@localhost/fastapi',echo=True)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)