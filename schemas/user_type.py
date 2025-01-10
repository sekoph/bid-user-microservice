from pydantic import BaseModel
from datetime import datetime

class UserTypeBase(BaseModel):
    name: str
    
class CreateUserType(UserTypeBase):
    pass

class UserType(UserTypeBase):
    id: int
    date_created: datetime

    class Config:
        from_attributes = True