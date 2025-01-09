from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import database, schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#SECRET_KKEY
from dotenv import load_dotenv
from . import schemas
import os
load_dotenv()
#ALGORITHM 

#EXPIRAtion TERM


ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt


def verify_acess_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate", headers={"WWW_Authenticate": "Bearer"})
    token = verify_acess_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
