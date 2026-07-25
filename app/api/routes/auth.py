from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from app.schemas.users import UserCreate, UserLogin, UserResponse
from app.db.models import User
from app.core.security import hash_password, hash_verify, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

# Creating an instance of APIRouter:
router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    # if the user with this user name already exist:
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username already registered.")
    # if not then lets add this new user to the database:
    new_user = User(
        username=user.username,
        email=user.email, 
        hashed_passwords=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # username check:
    result = await db.execute(
        select(User).where(form_data.username == User.username)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Username or Password.")
    
    # veryfing password:
    verification = hash_verify(form_data.password, user.hashed_passwords)
    if not verification:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password.")
    
    access_token = create_access_token(data = {'sub':user.username})
    return {"access_token": access_token, "token_type": "bearer"}
    