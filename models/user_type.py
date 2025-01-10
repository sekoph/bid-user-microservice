from sqlalchemy import Column, Integer, String, DateTime,func
from sqlalchemy.orm import relationship
from config.db import Base
import datetime

class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, index=True, nullable=False)
    date_created =  Column(DateTime, default=func.now())

    # relationship
    users = relationship("User", back_populates="user_type")






