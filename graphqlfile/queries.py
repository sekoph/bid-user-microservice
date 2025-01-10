import strawberry
from typing import List, Optional
from .types import UserTypeQl
from sqlalchemy.orm import Session
from models.user import User

@strawberry.type
class Query:
    @strawberry.field
    async def disabled_user(self, info) -> List[UserTypeQl]:
        db:Session = info.context['db']
        users = db.query(User).filter(User.disabled == True).all()
        return [
            UserTypeQl(
                id = user.id,
                username= user.username,
                email= user.email,
                name= user.name,
                disabled= user.disabled,
                date_created= user.date_created
            )
            for user in users
        ]
        
        

    @strawberry.field
    async def enabled_user(self, info) -> List[UserTypeQl]:
        db: Session = info.context["db"]
        users = db.query(User).filter(User.disabled == False).all()
        return [
            UserTypeQl(
                id = user.id,
                username= user.username,
                email= user.email,
                name= user.name,
                disabled= user.disabled,
                date_created= user.date_created
            )
            for user in users
        ]