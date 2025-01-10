from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
import fastapi.security as _security
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
import logging
from sqlalchemy.orm import Session
import models.user
from schemas.user import User,TokenData
import models
from datetime import timedelta, datetime
from security.database import get_db
from crud.user import get_user_by_username


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "4e35adf759f7b1302f623a450d41d0962d37dce6ed44c13b87f3fd839caf1967"
ALGORITHM = "HS256"


oauth2_scheme = _security.OAuth2PasswordBearer(tokenUrl="/login_token")

# for admin login
oauth2_scheme2 = _security.OAuth2PasswordBearer(tokenUrl="/admin/login_token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.user.User).filter(models.user.User.username == username).first()
    # user = get_user_by_username(db = db, username= username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except JWTError as e:
        raise credentials_exception
    
    try:
        user = await get_user_by_username(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    
    
async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except JWTError as e:
        raise credentials_exception
    
    try:
        user = await get_user_by_username(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user


async def get_current_active_admin(current_user: User = Depends(get_current_admin)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user