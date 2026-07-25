from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Creating an account/registering:
class UserCreate(BaseModel):
    username: str = Field(description="Please enter your username")
    email: EmailStr = Field(description="Please enter your email")
    password: str = Field(description="Must be at least 8 characters")

# User login/login:
class UserLogin(BaseModel):
    username: str = Field(
        description="Please enter your username"
)
    password: str = Field(
        description="Please enter your password"
)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True