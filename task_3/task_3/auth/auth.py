from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
import models,schemas
from sqlalchemy.orm import session
from database import get_db
from typing import Annotated


setting=schemas.Setting()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:session=Depends(get_db)):
    """to get user information from payload of jwt and in this case username  """

    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate" :"Bearer"},
    )
    try:
        payload=jwt.decode(token,setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        name:str=payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data=schemas.TokenData(name=name)
    except JWTError:
        raise credentials_exception
    print(token_data.name)
    user=db.query(models.User).filter(models.User.name==token_data.name).first()
    if user is None:
        raise credentials_exception
    return user