from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2AuthorizationCodeBearer , OAuth2PasswordRequestForm

from schemas.user import CreateUser,UpdateUser
from models.user import User
from fastapi import HTTPException
from crud.user_type import get_user_type_by_name


# select user by id
async def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# get users by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

async def get_user_by_username(db:Session, username: str):
    return db.query(User).filter(User.username == username).first()


# get all users
def get_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()


# create users
def Create_User(db: Session, user: CreateUser, user_type_id: int, disabled: bool):
    try:
        new_user = User(name=user.name, username = user.username, email = user.email, hashed_password = user.password, user_type_id = user_type_id, disabled = disabled)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        return False
    

# update user status
def Update_User(db:Session, user:UpdateUser, user_id: int):
    user_check = db.query(User).filter(User.id == user_id).first()
    if user_check:
        for key,value in user.dict(exclude_unset= True).items():
            setattr(user_check,key,value)
        db.commit()
        db.refresh(user_check)
    return user_check

        


# delete user
def Delete_User(db:Session,user_id:int):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete


# def get_user_userType(db:Session, user_type_id:int):
#     user = get_user_type_by_name(db:Session,name="admin")
#     return db.query(User).filter(User.user_type_id == user_type_id).first()
