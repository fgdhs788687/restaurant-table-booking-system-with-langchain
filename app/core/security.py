from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt 
from app.core.config import settings

def current_time():
    return datetime.now(timezone.utc)


# Password hashing context:
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)

# Hashing utilities:
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verification utilities:
def hash_verify(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)



# Token utilities:
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = current_time() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

def decode_access_token(token: str):
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm]
    )