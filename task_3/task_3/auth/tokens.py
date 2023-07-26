from fastapi import Depends
from jose import JWTError,jwt
from datetime import datetime,timedelta
from sqlalchemy.orm import session
from database import get_db
from .hashing import verify_password
import schemas,models

setting=schemas.Setting()
def authenticate_user(username: str, password: str,db:session=Depends(get_db)):
    """"this function authenticate the users by comparing database value and the OAuth2PasswordRequestForm values """
    user = db.query(models.User).filter(models.User.name==username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):

    """"to create jwt token for name"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt
