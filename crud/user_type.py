from sqlalchemy.orm import Session
from schemas.user_type import CreateUserType
from models.user_type import UserType
from sqlalchemy.exc import IntegrityError


def create_user_type(db: Session, userType: CreateUserType):
    try:
        new_user_type = UserType(name= userType.name)
        db.add(new_user_type)
        db.commit()
        db.refresh(new_user_type)
        return new_user_type
    except IntegrityError:
        db.rollback()
        return False
    
    
def get_user_type(db:Session, skip:int, limit:int):
    return db.query(UserType).offset(skip).limit(limit).all()


async def get_user_type_by_name(db:Session, name:str):
    return db.query(UserType).filter(UserType.name == name).first()
