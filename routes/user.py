from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from config.db import SessionLocal
from crud.user import Create_User, get_users,get_user_by_email,Update_User,Delete_User,get_user_by_id, get_user_by_username
from schemas.user import User, CreateUser,Token, UpdateUser
import security.auth

# from routes.custome_oauth import OAuth2EmailRequestForm
from datetime import datetime,timedelta
import models.user
from crud.user_type import get_user_type_by_name

ACCESS_TOKEN_EXPIRE_MINUTES = 30

usersRouter = APIRouter()

# define database dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""user routers"""

# create new user
@usersRouter.post('/create_user', response_model = User)
async def create_user(new_user: CreateUser, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db = db , email = new_user.email)
    user_username = await get_user_by_username(db,username=new_user.username)
    if db_user and user_username:
        raise HTTPException(status_code = 400, detail="email or password exists")
    hashed_password = security.auth.get_password_hash(new_user.password)
    new_user.password = hashed_password
    return Create_User(db = db, user = new_user, user_type_id = 1, disabled = False)


# get all users
@usersRouter.get('/get_users', response_model = list[User])
async def users(skip : int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_user)):
    return get_users(db, skip = skip, limit = limit)


# get user by email
@usersRouter.get('/get_user/{email}', response_model = User)
async def get_user(email: str, db: Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_user)):
    user = get_user_by_email(db = db , email = email)
    if user is None:
        raise HTTPException(status_code= 404, detail="user does not exist")
    return user


#login access token
@usersRouter.post('/login_token',response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = security.auth.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@usersRouter.get("/api/user/me", response_model=User)
async def read_users_me(current_user: User = Depends(security.auth.get_current_active_user)):
    try:
        # print(current_user.id)
        return current_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    



"admin routers"

# admin login
@usersRouter.post('/admin/login_token',response_model=Token)
async def admin_login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # check if user is admin
    user_type_info = await get_user_type_by_name(db=db, name="admin")
    user_info = await get_user_by_username(db, form_data.username)
    
    if user_type_info.id != user_info.user_type_id:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="Not an Admin",
                            headers={"WWW-Authenticate": "Bearer"},)
    # function to login
    user = security.auth.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@usersRouter.delete("/admin/delete_user/{user_id}", response_model=User)
async def delete_user(user_id: int, db:Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_admin)):
    user = await get_user_by_id(db,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    Delete_User(db,user_id)
    return user


@usersRouter.put("/admin/activate_use/{user_id}", response_model=User)
async def update_user_status(user_id: int, user:UpdateUser, db:Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_admin)):
    user_to_update = Update_User(db,user,user_id)
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.model_validate(user_to_update)

@usersRouter.get("/get_admin/me", response_model=User)
async def read_users_me(current_user: User = Depends(security.auth.get_current_active_admin)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
