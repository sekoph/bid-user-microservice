from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import SessionLocal
from crud.user_type import create_user_type, get_user_type , get_user_type_by_name
from schemas.user_type import CreateUserType, UserType


# define database dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
usertypeRouter = APIRouter()


@usertypeRouter.post('/api/create_user_type', response_model=UserType)
def CreateUserType(user_type: CreateUserType, db: Session = Depends(get_db)):
    # db_user_type = get_user_type_by_name(db = db, name = user_type.__name__)
    
    # if db_user_type:
        # raise HTTPException(status_code=400, detail="name exists")
    return create_user_type(db, user_type)

@usertypeRouter.get('/api/get_user_type', response_model=list[UserType])
def getAllUserType(skip: int = 0, limit: int = 100, db:Session = Depends(get_db)):
    return get_user_type(db,skip=skip,limit=limit)