from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# base class for user
class UserBase(BaseModel):
    name: str
    username: str
    email: str

# to create user
class CreateUser(UserBase):
    password: str


#to update
class UpdateUser(BaseModel):
    disabled: Optional[bool]
    
    
#to pass all the user
class User(UserBase):
    id: int
    user_type_id: int
    date_created: datetime
    disabled: Optional[bool]


    
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    
class TokenData(BaseModel):
    username: str | None = None
