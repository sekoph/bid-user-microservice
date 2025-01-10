from sqlalchemy import Column , String, Integer, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from config.db import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, index=True, nullable=False)
    username = Column(String, index=True, unique=True,nullable= False)
    email =  Column(String,index= True, unique= True, nullable= False)
    hashed_password = Column(String ,nullable=False)
    disabled = Column(Boolean, default = False)
    user_type_id = Column(Integer, ForeignKey("user_type.id", ondelete="CASCADE"), nullable=False)
    date_created =  Column(DateTime, default=func.now())
    
    # relationship
    user_type = relationship("UserType", back_populates="users")
    

    